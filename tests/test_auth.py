"""F01 회원가입/인증 명세 검증."""

from tests.conftest import auth_header, register


async def test_check_nickname_available(client):
    resp = await client.get("/api/v1/auth/check-nickname", params={"nickname": "newbie1"})
    assert resp.status_code == 200
    assert resp.json() == {"available": True, "reason": None}


async def test_check_nickname_forbidden(client):
    # admin 은 마이그레이션 시드에 포함된 금칙어
    resp = await client.get("/api/v1/auth/check-nickname", params={"nickname": "admin"})
    assert resp.json() == {"available": False, "reason": "forbidden_word"}


async def test_check_nickname_invalid_format(client):
    resp = await client.get("/api/v1/auth/check-nickname", params={"nickname": "ab@c"})
    assert resp.json() == {"available": False, "reason": "invalid_format"}


async def test_signup_returns_token_and_recovery(client):
    data = await register(client, "tester1")
    assert "access_token" in data
    assert len(data["recovery_code"]) == 12
    assert data["token_type"] == "bearer"


async def test_signup_sets_refresh_cookie(client):
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "cookieuser", "password": "pass1234"}
    )
    assert "refresh_token" in resp.cookies


async def test_refresh_cookie_samesite_lax_when_not_secure(client, monkeypatch):
    from app.api.v1 import auth as auth_module

    monkeypatch.setattr(auth_module.settings, "COOKIE_SECURE", False)
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "cookielax", "password": "pass1234"}
    )
    set_cookie = resp.headers.get_list("set-cookie")[0]
    assert "samesite=lax" in set_cookie.lower()


async def test_refresh_cookie_samesite_none_when_secure(client, monkeypatch):
    from app.api.v1 import auth as auth_module

    monkeypatch.setattr(auth_module.settings, "COOKIE_SECURE", True)
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "cookienone", "password": "pass1234"}
    )
    set_cookie = resp.headers.get_list("set-cookie")[0]
    assert "samesite=none" in set_cookie.lower()


async def test_signup_weak_password_rejected(client):
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "weakpw", "password": "onlyletters"}
    )
    assert resp.status_code == 422


async def test_signup_duplicate_nickname(client):
    await register(client, "dupuser")
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "dupuser", "password": "pass1234"}
    )
    assert resp.status_code == 409


async def test_signup_forbidden_nickname(client):
    resp = await client.post(
        "/api/v1/auth/signup", json={"nickname": "admin", "password": "pass1234"}
    )
    assert resp.status_code == 409


async def test_login_needs_onboarding_flips(client):
    await register(client, "onboard1")

    login = await client.post(
        "/api/v1/auth/login", json={"nickname": "onboard1", "password": "pass1234"}
    )
    assert login.status_code == 200
    body = login.json()
    assert body["needs_onboarding"] is True

    # 모드 설정 후 재로그인 → needs_onboarding=false
    await client.put(
        "/api/v1/users/me/mode",
        json={"mode": "visual"},
        headers=auth_header(body["access_token"]),
    )
    login2 = await client.post(
        "/api/v1/auth/login", json={"nickname": "onboard1", "password": "pass1234"}
    )
    assert login2.json()["needs_onboarding"] is False


async def test_login_wrong_password(client):
    await register(client, "wrongpw")
    resp = await client.post(
        "/api/v1/auth/login", json={"nickname": "wrongpw", "password": "bad12345"}
    )
    assert resp.status_code == 401


async def test_refresh_with_cookie(client):
    await register(client, "refresher")
    # signup 응답에서 쿠키가 client jar 에 저장됨 → refresh 시 자동 전송
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_refresh_without_cookie(client):
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 401


async def test_recovery_resets_password(client):
    data = await register(client, "recover1", password="old12345")
    resp = await client.post(
        "/api/v1/auth/recovery",
        json={
            "nickname": "recover1",
            "recovery_code": data["recovery_code"],
            "new_password": "new12345",
        },
    )
    assert resp.status_code == 200
    # 새 비번 로그인 성공
    login = await client.post(
        "/api/v1/auth/login", json={"nickname": "recover1", "password": "new12345"}
    )
    assert login.status_code == 200


async def test_recovery_wrong_code(client):
    await register(client, "recover2")
    resp = await client.post(
        "/api/v1/auth/recovery",
        json={
            "nickname": "recover2",
            "recovery_code": "WRONGCODE123",
            "new_password": "new12345",
        },
    )
    assert resp.status_code == 401


async def test_me_requires_auth(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


async def test_me_returns_profile(client):
    data = await register(client, "profileme")
    resp = await client.get("/api/v1/auth/me", headers=auth_header(data["access_token"]))
    assert resp.status_code == 200
    body = resp.json()
    assert body["nickname"] == "profileme"
    assert body["disability_mode"] is None
    assert body["trust_score"] == 1.0
