"""Redis TTL 쿼터 (VISION-01·CAPTION-01 호출 한도)."""

import pytest_asyncio
import redis.asyncio as aioredis

from app.core.config import settings
from app.services.quota import caption_key, refund, try_consume, vision_keys


@pytest_asyncio.fixture
async def redis():
    base = settings.REDIS_URL.rsplit("/", 1)[0]
    r = aioredis.from_url(f"{base}/1", decode_responses=True)
    await r.flushdb()
    yield r
    await r.aclose()


async def test_try_consume_respects_limit(redis):
    for _ in range(3):
        assert await try_consume(redis, "q:test", limit=3, ttl_seconds=60)
    assert not await try_consume(redis, "q:test", limit=3, ttl_seconds=60)


async def test_refund_restores_slot(redis):
    for _ in range(3):
        await try_consume(redis, "q:test", limit=3, ttl_seconds=60)
    await refund(redis, "q:test")  # CAPTION-01: 자막 실패 시 횟수 복원
    assert await try_consume(redis, "q:test", limit=3, ttl_seconds=60)


def test_key_builders():
    keys = vision_keys("u1")
    assert len(keys) == 2
    day, minute = keys
    assert day[1] == settings.VISION_DAILY_LIMIT
    assert minute[1] == settings.VISION_MINUTE_LIMIT
    ckey = caption_key("u1")
    assert ckey[1] == settings.CAPTION_DAILY_LIMIT
