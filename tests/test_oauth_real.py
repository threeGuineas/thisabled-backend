"""실 제공자(카카오·구글) OAuth 경로 — 외부 API를 MockTransport로 대체해 검증.

실키 없이 코드 경로(파라미터 인코딩·토큰 교환·오류 매핑)를 고정한다.
실키 스모크 테스트는 docs/oauth-setup.md 절차로 별도 수행.
"""

from urllib.parse import parse_qs, quote

import httpx
import pytest

from app.core.config import settings
from app.services import oauth as oauth_mod
from tests.conftest import auth_header, callback_params


@pytest.fixture
def real_oauth(monkeypatch):
    """OAUTH_MOCK 해제 + 테스트용 가짜 키 주입."""
    monkeypatch.setattr(settings, "OAUTH_MOCK", False)
    monkeypatch.setattr(settings, "KAKAO_CLIENT_ID", "kakao-test-id")
    monkeypatch.setattr(settings, "KAKAO_CLIENT_SECRET", "")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "google-test-id")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", "google-test-secret")
    return monkeypatch


def _kakao_transport(valid_code: str = "kakao-auth-code"):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "kauth.kakao.com" and request.url.path == "/oauth/token":
            form = parse_qs(request.content.decode())
            assert form["client_id"] == ["kakao-test-id"]
            assert "client_secret" not in form  # 미설정 시 파라미터 자체를 생략
            if form.get("code") != [valid_code]:
                return httpx.Response(400, json={"error": "invalid_grant"})
            return httpx.Response(200, json={"access_token": "kakao-access-token"})
        if request.url.host == "kapi.kakao.com" and request.url.path == "/v2/user/me":
            assert request.headers["Authorization"] == "Bearer kakao-access-token"
            return httpx.Response(200, json={"id": 4242424242})
        return httpx.Response(404)

    return httpx.MockTransport(handler)


def _google_transport(valid_code: str = "google-auth-code"):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "oauth2.googleapis.com" and request.url.path == "/token":
            form = parse_qs(request.content.decode())
            assert form["client_id"] == ["google-test-id"]
            assert form["client_secret"] == ["google-test-secret"]
            if form.get("code") != [valid_code]:
                return httpx.Response(400, json={"error": "invalid_grant"})
            return httpx.Response(200, json={"access_token": "google-access-token"})
        if (
            request.url.host == "openidconnect.googleapis.com"
            and request.url.path == "/v1/userinfo"
        ):
            assert request.headers["Authorization"] == "Bearer google-access-token"
            return httpx.Response(200, json={"sub": "108864131868493822153"})
        return httpx.Response(404)

    return httpx.MockTransport(handler)


async def test_kakao_authorize_url_is_encoded(client, real_oauth):
    resp = await client.get("/api/v1/auth/kakao/authorize")
    assert resp.status_code == 200
    url = resp.json()["authorize_url"]
    assert url.startswith("https://kauth.kakao.com/oauth/authorize?")
    assert "client_id=kakao-test-id" in url
    # redirect_uri는 반드시 percent-encoding (스킴·슬래시 원문 금지)
    encoded = quote(f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/kakao/callback", safe="")
    assert f"redirect_uri={encoded}" in url


async def test_google_authorize_url_has_openid_scope(client, real_oauth):
    resp = await client.get("/api/v1/auth/google/authorize")
    assert resp.status_code == 200
    url = resp.json()["authorize_url"]
    assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
    assert "scope=openid" in url


async def test_kakao_callback_signup_then_login(client, real_oauth):
    real_oauth.setattr(oauth_mod, "_transport", _kakao_transport())

    # 1) 최초 콜백 → 신규 사용자, signup_token을 담아 프론트로 302
    cb = await client.get("/api/v1/auth/kakao/callback?code=kakao-auth-code")
    params = callback_params(cb)
    assert params["is_new_user"] == "true"

    # 2) 추가 정보 입력으로 가입 완료
    signup = await client.post(
        "/api/v1/auth/signup",
        json={
            "signup_token": params["signup_token"],
            "nickname": "카카오유저",
            "birth_date": "2000-01-01",
            "ui_mode": "visual",
            "agreements": {"terms": True, "privacy": True, "ai_notice": True},
        },
    )
    assert signup.status_code == 201, signup.text
    token = signup.json()["access_token"]
    me = await client.get("/api/v1/users/me", headers=auth_header(token))
    assert me.json()["nickname"] == "카카오유저"

    # 3) 같은 카카오 계정 재콜백 → 즉시 로그인 리다이렉트
    again = await client.get("/api/v1/auth/kakao/callback?code=kakao-auth-code")
    params = callback_params(again)
    assert params["is_new_user"] == "false"
    assert params["access_token"]
    assert "refresh_token" in again.cookies


async def test_google_callback_uses_oidc_sub(client, real_oauth):
    real_oauth.setattr(oauth_mod, "_transport", _google_transport())
    cb = await client.get("/api/v1/auth/google/callback?code=google-auth-code")
    assert callback_params(cb)["is_new_user"] == "true"


async def test_invalid_code_redirects_with_error(client, real_oauth):
    """제공자가 거부한 code(만료·재사용)도 프론트로 error 리다이렉트."""
    real_oauth.setattr(oauth_mod, "_transport", _kakao_transport())
    cb = await client.get("/api/v1/auth/kakao/callback?code=expired-code")
    assert callback_params(cb)["error"] == "kakao_failed"


async def test_provider_network_error_redirects_with_error(client, real_oauth):
    """제공자 연결 불가(네트워크 장애)도 프론트로 error 리다이렉트."""

    def down(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    real_oauth.setattr(oauth_mod, "_transport", httpx.MockTransport(down))
    cb = await client.get("/api/v1/auth/kakao/callback?code=whatever")
    assert callback_params(cb)["error"] == "kakao_failed"


async def test_user_denial_redirects_with_error(client, real_oauth):
    """사용자가 제공자 동의 화면에서 거부하면 code 없이 error만 돌아온다."""
    cb = await client.get("/api/v1/auth/kakao/callback?error=access_denied")
    assert callback_params(cb)["error"] == "kakao_failed"
