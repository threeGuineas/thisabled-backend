"""§15 회원 탈퇴 — 익명화/삭제 선택, 채팅 보존, 30일 재가입 제한."""

import uuid

from sqlalchemy import select

from app.models import ChatMessage, ChatRoom, Post, User, WithdrawnSocial
from app.core.pairs import normalize_pair
from tests.conftest import auth_header, callback_params, register


async def _make_post(db, author_id) -> uuid.UUID:
    post = Post(id=uuid.uuid4(), author_id=author_id, content="탈퇴 테스트 글", status="published")
    db.add(post)
    await db.commit()
    return post.id


async def _make_chat(db, sender_id, receiver_id) -> uuid.UUID:
    a, b = normalize_pair(sender_id, receiver_id)
    room = ChatRoom(id=uuid.uuid4(), user_a=a, user_b=b, state="active")
    db.add(room)
    await db.flush()
    msg = ChatMessage(
        id=uuid.uuid4(), room_id=room.id, sender_id=sender_id,
        content="탈퇴 전 메시지", safety_status="safe",
    )
    db.add(msg)
    await db.commit()
    return msg.id


async def test_withdraw_anonymize_keeps_posts_and_chat(client, db):
    a = await register(client, "탈퇴자A", uid="wd-a")
    b = await register(client, "상대방B", uid="wd-b")
    a_id, b_id = uuid.UUID(a["user_id"]), uuid.UUID(b["user_id"])
    post_id = await _make_post(db, a_id)
    msg_id = await _make_chat(db, a_id, b_id)

    resp = await client.request(
        "DELETE", "/api/v1/users/me",
        json={"posts_action": "anonymize"}, headers=auth_header(a["access_token"]),
    )
    assert resp.status_code == 204, resp.text

    assert await db.get(User, a_id) is None  # 계정 즉시 삭제
    post = await db.get(Post, post_id)
    assert post is not None and post.author_id is None  # '탈퇴한 사용자'
    msg = await db.get(ChatMessage, msg_id)
    assert msg is not None and msg.sender_id is None  # 상대방 기록 보존 + 익명화
    assert msg.content == "탈퇴 전 메시지"

    withdrawn = (
        await db.execute(select(WithdrawnSocial).where(WithdrawnSocial.provider_user_id == "wd-a"))
    ).scalar_one()
    assert withdrawn.provider == "mock"


async def test_withdraw_delete_removes_posts(client, db):
    a = await register(client, "탈퇴자C", uid="wd-c")
    a_id = uuid.UUID(a["user_id"])
    post_id = await _make_post(db, a_id)

    resp = await client.request(
        "DELETE", "/api/v1/users/me",
        json={"posts_action": "delete"}, headers=auth_header(a["access_token"]),
    )
    assert resp.status_code == 204
    assert await db.get(Post, post_id) is None


async def test_withdraw_invalidates_token_and_blocks_rejoin(client):
    a = await register(client, "탈퇴자D", uid="wd-d")
    h = auth_header(a["access_token"])
    resp = await client.request("DELETE", "/api/v1/users/me", json={"posts_action": "anonymize"}, headers=h)
    assert resp.status_code == 204

    me = await client.get("/api/v1/users/me", headers=h)
    assert me.status_code == 401  # 토큰 무효

    # 동일 소셜 계정 30일 재가입 제한 (§15)
    cb = await client.get("/api/v1/auth/mock/callback?code=mock:wd-d")
    signup = await client.post("/api/v1/auth/signup", json={
        "signup_token": callback_params(cb)["signup_token"], "nickname": "재가입D",
        "birth_date": "2000-01-01", "ui_mode": "visual",
        "agreements": {"terms": True, "privacy": True, "ai_notice": True},
    })
    assert signup.status_code == 403
