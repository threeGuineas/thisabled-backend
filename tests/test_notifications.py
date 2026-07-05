"""§16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증."""

from tests.conftest import auth_header, register
from tests.test_chat import make_friends, _room, _send
from tests.test_safe import safety  # noqa: F401 — fixture 재사용


async def _notis(client, h):
    resp = await client.get("/api/v1/notifications", headers=h)
    assert resp.status_code == 200
    return resp.json()["items"]


async def test_comment_and_like_notify_author_not_self(client):
    a = await register(client, "알림작성자")
    b = await register(client, "알림댓글러")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    post = (await client.post("/api/v1/posts", json={"content": "알림 글"}, headers=ha)).json()

    # 본인 행동은 알림 없음
    await client.post(f"/api/v1/posts/{post['id']}/like", headers=ha)
    assert await _notis(client, ha) == []

    await client.post(f"/api/v1/posts/{post['id']}/comments", json={"content": "댓글"}, headers=hb)
    await client.post(f"/api/v1/posts/{post['id']}/like", headers=hb)
    types = [n["type"] for n in await _notis(client, ha)]
    assert "post.comment" in types and "post.like" in types


async def test_friend_request_and_accept_notifications(client):
    a = await register(client, "알림친구갑")
    b = await register(client, "알림친구을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    req = await client.post("/api/v1/friends/requests", json={"receiver_id": b["user_id"]}, headers=ha)
    assert [n["type"] for n in await _notis(client, hb)] == ["friend.request"]

    await client.post(f"/api/v1/friends/requests/{req.json()['id']}/accept", headers=hb)
    assert "friend.accepted" in [n["type"] for n in await _notis(client, ha)]


async def test_flagged_and_restriction_notify_receiver(client, safety):  # noqa: F811
    a = await register(client, "알림위험갑")
    b = await register(client, "알림위험을")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room = (await _room(client, ha, b["user_id"])).json()

    for i in range(3):
        await _send(client, ha, room["id"], f"돈 내놔 {i}")

    types = [n["type"] for n in await _notis(client, hb)]
    assert "chat.flagged" in types
    assert "chat.restricted" in types  # SAFE-05-5 수신자 안내
    # 발신자에게는 어떤 판정 알림도 없음 (비노출 원칙)
    assert all(n["type"] not in ("chat.flagged", "chat.restricted") for n in await _notis(client, ha))


async def test_mark_read(client):
    a = await register(client, "읽음유저")
    b = await register(client, "읽음상대")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await client.post("/api/v1/friends/requests", json={"receiver_id": b["user_id"]}, headers=ha)
    notis = await _notis(client, hb)
    assert notis[0]["read_at"] is None
    resp = await client.post("/api/v1/notifications/read", json={"ids": [notis[0]["id"]]}, headers=hb)
    assert resp.status_code == 200
    assert (await _notis(client, hb))[0]["read_at"] is not None
