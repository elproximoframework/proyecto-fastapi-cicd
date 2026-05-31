from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.v1.router import api_router
from src.app.core.config import settings
from src.app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización: Crear tablas si no se usa Alembic directamente en desarrollo local
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Limpieza: Cerrar conexiones
    await engine.dispose()


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de la versión 1 de la API
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Salud"])
async def health_check():
    """Endpoint básico para validar que el servicio está activo (usado por Docker/AWS)."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/version", tags=["Salud"])
async def get_version():
    """Retorna la versión actual de la API."""
    return {"version": settings.VERSION}
