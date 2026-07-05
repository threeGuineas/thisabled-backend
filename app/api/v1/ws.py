"""WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시.

인증은 JWT 검증만으로 처리(DB 미조회)해 연결 비용을 최소화한다.
구독 채널: user:{user_id} (app/services/events.py).
"""

import asyncio
import contextlib
import uuid

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from jose import JWTError

from app.core.security import decode_token
from app.db.redis import get_redis
from app.services.events import user_channel

router = APIRouter(tags=["ws"])

WS_UNAUTHORIZED = 4401


async def _relay(pubsub, websocket: WebSocket) -> None:
    async for message in pubsub.listen():
        if message["type"] == "message":
            await websocket.send_text(message["data"])


@router.websocket("/ws")
async def ws_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    redis: aioredis.Redis = Depends(get_redis),
):
    try:
        payload = decode_token(token, expected_type="access")
        user_id = uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        await websocket.accept()
        await websocket.close(code=WS_UNAUTHORIZED)
        return

    pubsub = redis.pubsub()
    await pubsub.subscribe(user_channel(user_id))
    await websocket.accept()
    relay = asyncio.create_task(_relay(pubsub, websocket))
    try:
        while True:
            # 클라이언트 수신 루프 — 연결 종료 감지용 (보내는 내용은 무시)
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        relay.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await relay
        await pubsub.unsubscribe(user_channel(user_id))
        await pubsub.aclose()
