# 🚀 Proyecto de Práctica CI/CD: API con FastAPI, Docker y Pytest

¡Bienvenido a tu entorno de práctica! Este es un proyecto backend completo, asíncrono y robusto construido con **FastAPI**, **PostgreSQL** y **Redis**. Ha sido diseñado específicamente para que puedas poner en práctica todas las lecciones del curso: desde el control de versiones con **Git** y políticas de calidad local con **Pre-commit hooks**, hasta la automatización completa con **GitHub Actions (CI/CD)**.

---

## 🛠️ Tecnologías del Proyecto

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Backend asíncrono y autodocumentado)
*   **Base de Datos:** [PostgreSQL](https://www.postgresql.org/) (usando SQLAlchemy asíncrono + `asyncpg`)
*   **Cache & Bloqueos:** [Redis](https://redis.io/)
*   **Empaquetado:** [Docker & Docker Compose](https://www.docker.com/) (Entornos de desarrollo, testing y prod aislados)
*   **Pruebas:** [Pytest](https://docs.pytest.org/) + `pytest-asyncio` + `pytest-cov` (cobertura del código)

---

## 📈 Guía de Práctica Paso a Paso

Sigue esta secuencia para aplicar de forma práctica los conceptos explicados en la guía [curso_git_cicd_fastapi.md](../curso_git_cicd_fastapi.md).

### Paso 1: Inicialización de tu Repositorio Git
Abre tu terminal en esta carpeta (`dev/`) e inicializa Git para comenzar a registrar el historial:
```bash
# 1. Inicializar repositorio
git init -b main

# 2. Comprobar que el .gitignore funciona (no deben listarse carpetas temporales)
git status -sb

# 3. Crear tu primer commit usando Conventional Commits
git add .
git commit -m "chore: initial project template for CI-CD practices"
```

### Paso 2: Crear una Rama de Funcionalidad (Branching)
Simula el flujo de trabajo profesional (GitHub Flow):
```bash
# Crear y cambiar a una rama de feature para agregar los Pre-commit hooks
git checkout -b chore/add-pre-commit-hooks
```

### Paso 3: Configurar y Ejecutar Pre-commit Hooks
Para asegurar que tu código mantenga la máxima calidad antes de permitir commits:
1.  **Crea el archivo `.pre-commit-config.yaml`** en esta carpeta raíz (`dev/`). Puedes basarte en el template proporcionado en la sección **2.3** de [curso_git_cicd_fastapi.md](../curso_git_cicd_fastapi.md):
    ```yaml
    repos:
      - repo: https://github.com/psf/black
        rev: 24.3.0
        hooks:
          - id: black
            language_version: python3.12
      - repo: https://github.com/PyCQA/isort
        rev: 5.13.2
        hooks:
          - id: isort
            args: ["--profile", "black"]
      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.6.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-merge-conflict
          - id: detect-private-key
    ```
2.  **Instala y activa los hooks**:
    ```bash
    # Instalar pre-commit en tu entorno Python
    pip install pre-commit

    # Instalar los hooks en la configuración de Git local
    pre-commit install

    # Ejecutar manualmente sobre todos los archivos por primera vez
    pre-commit run --all-files
    ```
3.  **Realiza el commit** (los hooks se ejecutarán automáticamente e impedirán el commit si hay errores de formato, arreglándolos al instante):
    ```bash
    git add .pre-commit-config.yaml
    git commit -m "chore: configure pre-commit hooks for formatting and quality"
    ```

### Paso 4: Fusión y Práctica de Conventional Commits
```bash
# Volver a main y fusionar los cambios
git checkout main
git merge chore/add-pre-commit-hooks --no-ff -m "chore: merge pre-commit configuration branch"
```

---

## 🐳 Levantamiento Local del Proyecto (Docker)

Puedes levantar la base de datos de desarrollo, Redis y la API con un único comando si tienes **Docker Desktop** instalado:

```bash
# 1. Levantar contenedores en segundo plano
docker compose -f docker/docker-compose.yml up --build -d

# 2. Ver el estado y los logs en tiempo real
docker compose -f docker/docker-compose.yml logs -f api
```

*   **API Local:** Accede a la documentación interactiva e interactúa con los endpoints en [http://localhost:8000/docs](http://localhost:8000/docs).
*   **Endpoints incluidos:**
    *   `POST /api/v1/users/` — Registro de nuevos usuarios.
    *   `POST /api/v1/auth/token` — Obtención de tokens de portador (Bearer JWT).
    *   `GET /api/v1/users/me` — Datos del perfil propio (protegido por token JWT).
    *   `POST /api/v1/products/` — Crear productos (asociados al usuario, protegido).
    *   `GET /api/v1/products/` — Listar todos los productos (público).
    *   `GET /health` — Verificación de salud de la API.

---

## 🧪 Ejecución de Pruebas (Pytest)

Las pruebas están configuradas para ejecutarse asíncronamente. En `docker-compose.yml` se incluye un servicio llamado `db_test` (PostgreSQL de prueba) en memoria (`tmpfs`) expuesto en el puerto **5433** para evitar colisiones con la BD de desarrollo (puerto **5432**).

### Opción A: Ejecutar pruebas localmente desde tu máquina
```bash
# 1. Asegúrate de tener levantado el contenedor de pruebas (db_test)
docker compose -f docker/docker-compose.yml up -d db_test

# 2. Instalar dependencias de desarrollo localmente
pip install -e ".[dev]"

# 3. Ejecutar suite de pruebas con reporte de cobertura
pytest
```

### Opción B: Ejecutar pruebas dentro del contenedor de pruebas
```bash
# Ejecutar pytest directamente sobre el stage test-runner del Dockerfile
docker build --target test-runner -t fastapi-test-runner -f docker/Dockerfile .
docker run --rm fastapi-test-runner
```

---

## 🚀 Configuración del Pipeline CI/CD (GitHub Actions)

Para completar tu entrenamiento práctico:
1.  Crea un repositorio en **GitHub**.
2.  Agrega el remoto a tu repositorio local: `git remote add origin https://github.com/tu-usuario/tu-repo.git`.
3.  Crea la carpeta de workflows en la raíz del proyecto:
    ```bash
    mkdir -p .github/workflows
    ```
4.  Crea el archivo `.github/workflows/ci.yml` y copia en él la configuración del pipeline del **punto 6.2** de la guía [curso_git_cicd_fastapi.md](../curso_git_cicd_fastapi.md) para automatizar la calidad de código, análisis de seguridad con Bandit y ejecución de tests en matrices multi-versión.
5.  ¡Haz `git push` a tu repositorio de GitHub y observa cómo tu pipeline cobra vida en la pestaña **Actions**!
