from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    RESULTS_DIR: str = "results"
    LOG_LEVEL: str = "INFO"
    MAX_FILE_SIZE: int = 52428800  # 50 MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Создаём папки при старте
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)