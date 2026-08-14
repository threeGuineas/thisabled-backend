import redis.asyncio as aioredis
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

router = APIRouter()


class HealthOut(BaseModel):
    status: str
    db: str
    redis: str


@router.get(
    "/health",
    response_model=HealthOut,
    responses={503: {"model": HealthOut, "description": "DB 또는 Redis 연결 실패"}},
)
async def health():
    result = {"status": "ok", "db": "unknown", "redis": "unknown"}

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        result["db"] = "ok"
    except Exception:
        result["db"] = "error"
        result["status"] = "degraded"

    redis = None
    try:
        redis = aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        result["redis"] = "ok"
    except Exception:
        result["redis"] = "error"
        result["status"] = "degraded"
    finally:
        if redis is not None:
            await redis.aclose()

    status_code = 200 if result["status"] == "ok" else 503
    return JSONResponse(status_code=status_code, content=result)
