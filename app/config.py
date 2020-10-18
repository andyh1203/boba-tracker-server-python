from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv


class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DATABASE: str
    REDIS_URL: str
    PORT: int
    SESSION_SECRET: str
    CORS_ORIGIN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    load_dotenv()
    return Settings()
