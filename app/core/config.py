from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost/fintechbank"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FinTechBank API"
    
    class Config:
        env_file = ".env"

settings = Settings()