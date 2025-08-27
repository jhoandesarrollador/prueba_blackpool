from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FinTechBank API"
    
    class Config:
        env_file = ".env"

settings = Settings()