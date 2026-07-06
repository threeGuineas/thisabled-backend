"""실시간 이벤트 — Redis pub/sub 팬아웃 (다중 워커에서도 사용자별 채널로 전달).

event 형식: {"type": "chat.message"|"chat.restricted"|"notification", "payload": {...}}
채팅 원문은 이벤트에 싣지 않는다 — 수신 측이 REST로 조회 (SAFE-03 블러 규칙 재사용).
"""

import json

import redis.asyncio as aioredis


def user_channel(user_id) -> str:
    return f"user:{user_id}"


async def publish_to_user(redis: aioredis.Redis, user_id, event: dict) -> None:
    await redis.publish(user_channel(user_id), json.dumps(event, default=str, ensure_ascii=False))
