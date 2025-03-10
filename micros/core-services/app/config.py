from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Enrollment API Director"
    APP_VERSION: str
    APP_URL: str
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    # MAIL_DRIVER: str
    # MAIL_HOST: str
    # MAIL_PORT: str
    # MAIL_USERNAME: str
    # MAIL_PASSWORD: str
    # MAIL_ENCRYPTION: str
    # MAIL_FROM_NAME: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    MICROS_HASH: str
    AESKEY: str
    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Usar lru_cache para mejorar el rendimiento de las configuraciones
@lru_cache()
def get_env():
    return Settings()

# Obtener las configuraciones desde el archivo .env
settings = get_env()
