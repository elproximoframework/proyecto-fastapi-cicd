from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.app.core.config import settings

# Crear motor asíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Constructor de sesiones asíncronas
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Clase Base Declarativa para modelos
class Base(DeclarativeBase):
    pass


# Generador/Dependencia de sesión de BD
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
