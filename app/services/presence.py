"""Redis TTL 기반 사용자 온라인 상태.

연결 수를 저장해 여러 탭을 지원하고, heartbeat가 끊기면 TTL로 자동 정리한다.
"""

import asyncio
import uuid

import redis.asyncio as aioredis

from app.core.config import settings


def presence_key(user_id: uuid.UUID) -> str:
    return f"presence:{user_id}"


async def mark_online(redis: aioredis.Redis, user_id: uuid.UUID) -> None:
    key = presence_key(user_id)
    async with redis.pipeline(transaction=True) as pipe:
        pipe.incr(key)
        pipe.expire(key, settings.PRESENCE_TTL_SECONDS)
        await pipe.execute()


async def refresh_presence(redis: aioredis.Redis, user_id: uuid.UUID) -> None:
    await redis.expire(presence_key(user_id), settings.PRESENCE_TTL_SECONDS)


async def mark_offline(redis: aioredis.Redis, user_id: uuid.UUID) -> None:
    key = presence_key(user_id)
    remaining = await redis.decr(key)
    if remaining <= 0:
        await redis.delete(key)
    else:
        await redis.expire(key, settings.PRESENCE_TTL_SECONDS)


async def online_statuses(
    redis: aioredis.Redis, user_ids: list[uuid.UUID]
) -> dict[uuid.UUID, bool]:
    if not user_ids:
        return {}
    async with redis.pipeline(transaction=False) as pipe:
        for user_id in user_ids:
            pipe.exists(presence_key(user_id))
        values = await pipe.execute()
    return dict(zip(user_ids, (bool(value) for value in values), strict=True))


async def heartbeat(redis: aioredis.Redis, user_id: uuid.UUID) -> None:
    interval = max(1, settings.PRESENCE_TTL_SECONDS // 3)
    while True:
        await asyncio.sleep(interval)
        await refresh_presence(redis, user_id)
