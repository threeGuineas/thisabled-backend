"""Redis TTL 카운터 — VISION-01·CAPTION-01 사용자별 호출 한도.

키는 날짜/분 단위로 자연 만료(TTL)되고, 자막 실패(재시도 소진) 시 refund로 복원한다.
"""

from datetime import datetime, timezone

import redis.asyncio as aioredis

from app.core.config import settings


async def try_consume(redis: aioredis.Redis, key: str, limit: int, ttl_seconds: int) -> bool:
    """카운터 1 증가. 한도 초과면 롤백 후 False."""
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, ttl_seconds)
    if count > limit:
        await redis.decr(key)
        return False
    return True


async def refund(redis: aioredis.Redis, key: str) -> None:
    """CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원."""
    if int(await redis.get(key) or 0) > 0:
        await redis.decr(key)


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _minute() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M")


def vision_keys(user_id) -> list[tuple[str, int, int]]:
    """이미지 1장 = 1회, 게시물·채팅 합산 (VISION-01). [(키, 한도, TTL), ...]"""
    return [
        (f"quota:vision:day:{user_id}:{_today()}", settings.VISION_DAILY_LIMIT, 86400),
        (f"quota:vision:min:{user_id}:{_minute()}", settings.VISION_MINUTE_LIMIT, 60),
    ]


def caption_key(user_id) -> tuple[str, int, int]:
    """영상 업로드 = 1회 차감, 게시물·채팅 합산 (CAPTION-01)."""
    return (f"quota:caption:day:{user_id}:{_today()}", settings.CAPTION_DAILY_LIMIT, 86400)
