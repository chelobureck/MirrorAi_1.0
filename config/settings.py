from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, List

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "MirrorAI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    # Безопасность
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # База данных
    USE_POSTGRES: str = "False"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "mirrorai"
    DATABASE_URL: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Gmail SMTP
    GMAIL_USER: str = "your-gmail-user"
    GMAIL_APP_PASSWORD: str = "your-gmail-app-password"

    # Google OAuth
    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    GOOGLE_REFRESH_TOKEN: str = "refresh-token"

    GOOGLE_OAUTH_MARKER:str = "google_oauth"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: str = "587"
    SMTP_USER: str = "smtp-user"

    # Окружение
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()