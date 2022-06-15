# shortener_app/config.py
from functools import lru_cache 

from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name : str = "local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache  # decorador de almacenaminto en cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Cargando setting para: {settings.env_name}")
    return settings

