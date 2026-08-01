"""
Settings module for Mega AI Agent.
Configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Literal
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

    #FILE_PATH: Path
    TEMP_FOLDER_NAME: str 
        
    # LLM Keys (optional in local/SQLite mode)
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    MODELS_JSON_PATH: str

    # Model Selection
    cooling_report_model: Optional[str] = None

    # Database — supports 'sqlite' (local) or 'postgres' (production)
    DATABASE_TYPE: Literal["sqlite", "postgres"] = "sqlite"
    DATABASE_URL: str = "sqlite:///./automep.db"

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_TYPE == "sqlite" or self.DATABASE_URL.startswith("sqlite")

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
