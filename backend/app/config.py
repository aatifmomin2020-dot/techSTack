import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Developer Portfolio Tech Stack Predictor"
    DEBUG: bool = True
    
    # Database configuration (Defaults to SQLite for local development, supports PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tech_stack_predictor.db")
    
    # Authentication
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-developer-tech-stack-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # External APIs
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
