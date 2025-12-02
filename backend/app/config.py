"""
Configurações do Backend
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # API Settings
    API_TITLE: str = "Newsletter FCP API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: list = [
      "http://localhost:3000",
      "http://localhost:5173",
      "https://app.nexteventsco.com"
    ]
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Email Settings (SMTP)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    # Tables
    LEADS_TABLE: str = "newsletter_leads"
    USERS_TABLE: str = "users_newsletter"

    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()
