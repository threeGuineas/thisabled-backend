"""WS 푸시 — 토큰 검증, pub/sub 릴레이, 채팅 전송 이벤트."""

import json
import uuid

import pytest
import redis as sync_redis
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.core.config import settings
from app.core.security import create_access_token
from app.main import app
from app.services.events import user_channel
from tests.conftest import auth_header, register
from tests.test_chat import make_friends, _room, _send, FakeSafety
from app.services.safety import get_safety_client

import pytest_asyncio


def test_ws_rejects_invalid_token():
    tc = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with tc.websocket_connect("/api/v1/ws?token=garbage") as ws:
            ws.receive_text()


def test_ws_relays_published_event():
    """운영 Redis(db 0)에 직접 publish — pub/sub은 잔존 데이터가 없어 안전."""
    user_id = uuid.uuid4()
    token = create_access_token(str(user_id))
    tc = TestClient(app)
    with tc.websocket_connect(f"/api/v1/ws?token={token}") as ws:
        r = sync_redis.Redis.from_url(settings.REDIS_URL)
        r.publish(user_channel(user_id), json.dumps({"type": "test.ping", "payload": {}}))
        data = json.loads(ws.receive_text())
        assert data["type"] == "test.ping"
        r.close()


@pytest_asyncio.fixture
async def safety():
    fake = FakeSafety()
    app.dependency_overrides[get_safety_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_safety_client, None)


async def test_chat_send_publishes_event(client, test_redis, safety):
    a = await register(client, "이벤트갑")
    b = await register(client, "이벤트을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()

    pubsub = test_redis.pubsub()
    await pubsub.subscribe(user_channel(b["user_id"]))
    try:
        await _send(client, ha, room["id"], "이벤트 확인")
        msg = None
        for _ in range(5):  # 첫 호출은 구독 확인 소비로 None일 수 있음
            msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if msg is not None:
                break
        assert msg is not None
        event = json.loads(msg["data"])
        assert event["type"] == "chat.message"
        assert event["payload"]["room_id"] == room["id"]
        assert "content" not in event["payload"]  # 원문 미포함
    finally:
        await pubsub.unsubscribe(user_channel(b["user_id"]))
        await pubsub.aclose()
