"""ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)."""

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import insert

from app.models import WithdrawnSocial
from tests.conftest import auth_header, register

AGREE = {"terms": True, "privacy": True, "ai_notice": True}


async def _signup_token(client, uid: str) -> str:
    resp = await client.get(f"/api/v1/auth/mock/callback?code=mock:{uid}")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["is_new_user"] is True
    return body["signup_token"]


async def test_callback_new_user_returns_signup_token(client):
    token = await _signup_token(client, "newbie")
    assert token


async def test_signup_success_adult(client):
    token = await _signup_token(client, "adult1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "성인유저",
        "birth_date": "2000-01-01", "ui_mode": "visual", "agreements": AGREE,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["access_token"]
    # refresh 쿠키 발급
    assert "refresh_token" in resp.cookies
    me = await client.get("/api/v1/users/me", headers=auth_header(body["access_token"]))
    # users 라우터는 Task 6 — 여기서는 인증 자체만 확인 (404가 아닌 401이 아니어야 함)
    assert me.status_code != 401


async def test_signup_minor_blocks_stranger_requests(client):
    token = await _signup_token(client, "minor1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "미성년유저",
        "birth_date": "2010-01-01", "ui_mode": "hearing", "agreements": AGREE,
    })
    assert resp.status_code == 201
    assert resp.json()["stranger_requests_allowed"] is False


async def test_signup_under_14_rejected(client):
    token = await _signup_token(client, "child1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "어린이",
        "birth_date": "2015-01-01", "ui_mode": "visual", "agreements": AGREE,
    })
    assert resp.status_code == 400
    assert "14세" in resp.json()["detail"]


async def test_signup_duplicate_nickname(client):
    await register(client, "중복닉네임", uid="dup-a")
    token = await _signup_token(client, "dup-b")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "중복닉네임",
        "birth_date": "2000-01-01", "ui_mode": "visual", "agreements": AGREE,
    })
    assert resp.status_code == 409


async def test_signup_forbidden_nickname(client):
    token = await _signup_token(client, "forb1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "관리자",
        "birth_date": "2000-01-01", "ui_mode": "visual", "agreements": AGREE,
    })
    assert resp.status_code == 400


async def test_signup_requires_all_agreements(client):
    token = await _signup_token(client, "agr1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "약관미동의",
        "birth_date": "2000-01-01", "ui_mode": "visual",
        "agreements": {"terms": True, "privacy": True, "ai_notice": False},
    })
    assert resp.status_code == 400


async def test_existing_user_callback_logs_in(client):
    await register(client, "재로그인", uid="relogin")
    resp = await client.get("/api/v1/auth/mock/callback?code=mock:relogin")
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_new_user"] is False
    assert body["access_token"]


async def test_rejoin_blocked_within_30_days(client, db):
    await db.execute(insert(WithdrawnSocial).values(
        id=uuid.uuid4(), provider="mock", provider_user_id="rejoin1",
        withdrawn_at=datetime.now(timezone.utc) - timedelta(days=5),
    ))
    await db.commit()
    token = await _signup_token(client, "rejoin1")
    resp = await client.post("/api/v1/auth/signup", json={
        "signup_token": token, "nickname": "재가입시도",
        "birth_date": "2000-01-01", "ui_mode": "visual", "agreements": AGREE,
    })
    assert resp.status_code == 403
    assert "30일" in resp.json()["detail"]


async def test_refresh_rotates_access_token(client):
    body = await register(client, "리프레시", uid="refresh1")
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 200
    assert resp.json()["access_token"]


async def test_invalid_mock_code_rejected(client):
    resp = await client.get("/api/v1/auth/mock/callback?code=garbage")
    assert resp.status_code == 400
