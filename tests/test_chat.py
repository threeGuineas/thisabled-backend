"""CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)."""

import pytest_asyncio

from app.main import app
from app.services import ai_media
from app.services.safety import SafetyUnavailable, get_safety_client
from tests.conftest import auth_header, register

PNG = b"\x89PNG\r\n\x1a\n" + b"1" * 32


class FakeSafety:
    """'돈' 포함 → flagged. fail=True → SafetyUnavailable (§18.3)."""

    def __init__(self):
        self.fail = False

    async def analyze(self, text: str, *, receiver_is_minor: bool) -> str:
        if self.fail:
            raise SafetyUnavailable()
        return "flagged" if "돈" in text else "safe"


@pytest_asyncio.fixture
async def safety():
    fake = FakeSafety()
    app.dependency_overrides[get_safety_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_safety_client, None)


async def _describe_fake():
    async def caller(*a, **k):
        return "채팅 사진 설명"
    return caller


async def make_friends(client, ha, hb, receiver_id):
    req = await client.post("/api/v1/friends/requests", json={"receiver_id": receiver_id}, headers=ha)
    await client.post(f"/api/v1/friends/requests/{req.json()['id']}/accept", headers=hb)


async def _room(client, h, user_id):
    return await client.post("/api/v1/chat/rooms", json={"user_id": user_id}, headers=h)


async def _send(client, h, room_id, content):
    return await client.post(f"/api/v1/chat/rooms/{room_id}/messages", json={"content": content}, headers=h)


async def test_friend_chat_roundtrip(client, safety):
    a = await register(client, "채팅갑")
    b = await register(client, "채팅을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])

    room = await _room(client, ha, b["user_id"])
    assert room.status_code == 200, room.text
    assert room.json()["state"] == "active"  # 친구 = 즉시 일반 채팅
    room_id = room.json()["id"]

    sent = await _send(client, ha, room_id, "안녕!")
    assert sent.status_code == 201
    assert sent.json()["safety_status"] is None  # 발신자에게 판정 비노출 (SAFE-03)

    msgs = await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)
    items = msgs.json()["items"]
    assert items[0]["content"] == "안녕!"
    assert items[0]["blurred"] is False

    rooms_b = await client.get("/api/v1/chat/rooms", headers=hb)
    assert len(rooms_b.json()["items"]) == 1
    assert rooms_b.json()["items"][0]["counterpart"]["nickname"] == "채팅갑"


async def test_stranger_request_flow(client, safety):
    a = await register(client, "낯선갑")
    b = await register(client, "낯선을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])

    room = await _room(client, ha, b["user_id"])
    assert room.json()["state"] == "request"  # 요청함 분리 (CHAT-02)
    room_id = room.json()["id"]

    assert (await _send(client, ha, room_id, "처음 인사드려요")).status_code == 201
    second = await _send(client, ha, room_id, "한 번 더")
    assert second.status_code == 400  # 수락 전 텍스트 1건만

    inbox = await client.get("/api/v1/chat/requests", headers=hb)
    assert len(inbox.json()["items"]) == 1

    # 수신자가 수락해야 일반 채팅 전환
    accept = await client.post(f"/api/v1/chat/requests/{room_id}/accept", headers=hb)
    assert accept.status_code == 200
    assert accept.json()["state"] == "active"
    assert (await _send(client, ha, room_id, "이제 됩니다")).status_code == 201


async def test_minor_default_blocks_adult_stranger(client, safety):
    adult = await register(client, "성인낯선", birth="1995-01-01")
    minor = await register(client, "미성년수신", birth="2010-01-01")
    ha = auth_header(adult["access_token"])
    room = await _room(client, ha, minor["user_id"])
    assert room.status_code == 404
    assert room.json()["detail"] == "요청을 보낼 수 없는 상대입니다"  # 사유 비노출


async def test_media_only_between_adult_friends(client, safety):
    adult1 = await register(client, "성인친구일", birth="1995-01-01")
    adult2 = await register(client, "성인친구이", birth="1994-01-01")
    minor = await register(client, "미성년친구", birth="2010-01-01")
    h1, h2 = auth_header(adult1["access_token"]), auth_header(adult2["access_token"])
    hm = auth_header(minor["access_token"])
    await make_friends(client, h1, h2, adult2["user_id"])
    await make_friends(client, h1, hm, minor["user_id"])

    describe = await _describe_fake()
    app.dependency_overrides[ai_media.get_describe_caller] = lambda: describe
    try:
        # 성인-성인 친구: 사진 전송 허용, 즉시 전달 + 설명 비동기 부착 (VISION-01)
        room = (await _room(client, h1, adult2["user_id"])).json()
        ok = await client.post(
            f"/api/v1/chat/rooms/{room['id']}/media",
            files={"file": ("c.png", PNG, "image/png")}, headers=h1,
        )
        assert ok.status_code == 201, ok.text
        msgs = (await client.get(f"/api/v1/chat/rooms/{room['id']}/messages", headers=h2)).json()
        assert msgs["items"][0]["type"] == "image"
        assert msgs["items"][0]["description"] == "채팅 사진 설명"

        # 미성년-성인 친구: 사진·동영상 전송 제한 (§4.5)
        room_m = (await _room(client, h1, minor["user_id"])).json()
        blocked = await client.post(
            f"/api/v1/chat/rooms/{room_m['id']}/media",
            files={"file": ("c.png", PNG, "image/png")}, headers=h1,
        )
        assert blocked.status_code == 403
    finally:
        app.dependency_overrides.pop(ai_media.get_describe_caller, None)


async def test_media_blocked_in_request_room(client, safety):
    a = await register(client, "요청미디어")
    b = await register(client, "요청수신자")
    ha = auth_header(a["access_token"])
    room = (await _room(client, ha, b["user_id"])).json()
    resp = await client.post(
        f"/api/v1/chat/rooms/{room['id']}/media",
        files={"file": ("c.png", PNG, "image/png")}, headers=ha,
    )
    assert resp.status_code == 403  # 수락 전 사진·동영상 불가 (CHAT-02)


async def test_opening_latest_messages_marks_unread_and_receipt(client, safety):
    a = await register(client, "읽음발신")
    b = await register(client, "읽음수신")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room_id = (await _room(client, ha, b["user_id"])).json()["id"]
    await _send(client, ha, room_id, "첫 메시지")
    await _send(client, ha, room_id, "두 번째 메시지")

    inbox = (await client.get("/api/v1/chat/rooms", headers=hb)).json()
    assert inbox["unread_total"] == 2
    assert inbox["items"][0]["unread_count"] == 2
    before = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=ha)).json()
    assert [item["is_read"] for item in before["items"]] == [False, False]

    await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)
    after = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=ha)).json()
    assert (await client.get("/api/v1/chat/rooms", headers=hb)).json()["unread_total"] == 0
    assert [item["is_read"] for item in after["items"]] == [True, False]


async def test_message_made_available_after_read_cursor_is_unread(client, db, safety):
    a = await register(client, "보류발신")
    b = await register(client, "보류수신")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room_id = (await _room(client, ha, b["user_id"])).json()["id"]

    from app.models import ChatMessage
    from datetime import datetime, timezone

    delayed = ChatMessage(
        room_id=__import__("uuid").UUID(room_id), sender_id=__import__("uuid").UUID(a["user_id"]),
        type="text", content="나중에 표시되는 메시지", safety_status="pending",
    )
    db.add(delayed)
    await db.commit()
    await _send(client, ha, room_id, "먼저 읽은 메시지")
    await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)
    delayed.safety_status = "safe"
    delayed.available_at = datetime.now(timezone.utc)
    await db.commit()

    inbox = (await client.get("/api/v1/chat/rooms", headers=hb)).json()
    assert inbox["unread_total"] == 1
