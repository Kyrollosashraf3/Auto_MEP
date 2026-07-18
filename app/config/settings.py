"""
Settings module for Mega AI Agent.
Configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str = ""
    DEBUG: bool
    HOST: str
    PORT: int

    FILE_ALLOWED_TYPES: List[str]
    FILE_ALLOWED_SIZE: int 

    FILE_PATH: Path

        
    # LLM  
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    GROQ_API_KEY: str
    MODELS_JSON_PATH: str
    


    # PostgreSQL
    DATABASE_URL: str

    # JWT Authentication
    SECRET_KEY: str = "supersecretkey_for_development_only_please_change"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'
    )

# Create singleton instance
settings = Settings()
