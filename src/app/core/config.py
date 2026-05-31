from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "mi-api-fastapi"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Seguridad
    SECRET_KEY: str = "development-only-super-secret-key-do-not-use-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Bases de datos
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/apidb"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Entorno
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
