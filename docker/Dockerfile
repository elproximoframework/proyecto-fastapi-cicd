# ── Stage 1: Builder ────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar algunas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo el pyproject.toml para descargar/compilar dependencias (cache layer)
COPY pyproject.toml .

# Crear wheels de las dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels ".[dev]"

# ── Stage 2: Test Runner ─────────────────────────────────────────
FROM python:3.12-slim AS test-runner
WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY pyproject.toml .
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl && \
    rm -rf /wheels

COPY . .
# Este stage se usa en CI para correr pruebas antes de construir la imagen final
CMD ["pytest", "tests/"]

# ── Stage 3: Production ───────────────────────────────────────────
FROM python:3.12-slim AS production

WORKDIR /app

# Usuario no root por seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /app/wheels /wheels
COPY pyproject.toml .
COPY src/ ./src/

# Instalar solo dependencias de ejecución (sin las de desarrollo)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-index --find-links=/wheels fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings python-jose passlib python-multipart asyncpg redis && \
    rm -rf /wheels

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
