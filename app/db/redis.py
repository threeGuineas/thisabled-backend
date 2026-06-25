import redis.asyncio as aioredis

from app.core.config import settings

_redis: aioredis.Redis | None = None


def get_redis_client() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def get_redis() -> aioredis.Redis:
    """FastAPI 의존성. 테스트에서 override 가능하도록 분리."""
    return get_redis_client()
