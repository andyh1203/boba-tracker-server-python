import redis
from app.config import get_settings
from functools import lru_cache

settings = get_settings()


@lru_cache
def get_redis_client():
    redis_client = redis.Redis(host=settings.REDIS_URL)
