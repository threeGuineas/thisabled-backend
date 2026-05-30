from fastapi import APIRouter
from sqlalchemy import text
import redis.asyncio as aioredis

from app.db.session import engine
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health():
    result = {"status": "ok", "db": "unknown", "redis": "unknown"}

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        result["db"] = "ok"
    except Exception as e:
        result["db"] = f"error: {e}"
        result["status"] = "degraded"

    try:
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        result["redis"] = "ok"
    except Exception as e:
        result["redis"] = f"error: {e}"
        result["status"] = "degraded"

    return result
