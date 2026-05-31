import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.app.core.config import settings
from src.app.core.database import Base, get_db
from src.app.main import app

# Cargar URL de la base de datos de test de variables de entorno o usar local (puerto 5433 expuesto para tests)
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5433/testdb"
)

# Crear motor asíncrono para la base de datos de pruebas
engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    """Crea y limpia la base de datos de pruebas (al inicio y final de la suite)."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine_test.dispose()


@pytest_asyncio.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
    """Sesión de base de datos para cada test con rollback automático."""
    async_session = AsyncSession(engine_test, expire_on_commit=False)
    async with async_session as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cliente asíncrono HTTPX con la sesión de base de datos de prueba inyectada."""
    async def override_get_db():
        yield db_session

    # Inyectar dependencia
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # Limpiar inyección
    app.dependency_overrides.clear()


@pytest.fixture
def user_payload():
    """Datos de prueba estándar para registrar un usuario."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
    }
