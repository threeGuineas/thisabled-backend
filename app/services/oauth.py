"""소셜 OAuth 제공자 추상화 (ACC-01).

- dev: OAUTH_MOCK=true → 모든 제공자 이름이 MockProvider로 동작 (키 불필요)
- prod: 카카오/구글 실키를 환경변수로 주입하고 OAUTH_MOCK=false
생년월일은 제공자에게 받지 않고 가입 추가정보에서 직접 입력받으므로
카카오 비즈 앱 전환 없이 계정 식별자만 사용한다.
"""

from dataclasses import dataclass
from typing import Protocol

import httpx
from fastapi import HTTPException

from app.core.config import settings


@dataclass
class OAuthUserInfo:
    provider: str
    provider_user_id: str


class OAuthProvider(Protocol):
    name: str

    def authorize_url(self, state: str) -> str: ...

    async def exchange_code(self, code: str) -> OAuthUserInfo: ...

    async def unlink(self, provider_user_id: str) -> None: ...


class MockProvider:
    """dev 전용. code 형식: `mock:<provider_user_id>`."""

    def __init__(self, name: str = "mock"):
        self.name = name

    def authorize_url(self, state: str) -> str:
        # 실제 리다이렉트 없이 콜백 URL을 그대로 안내 — FE가 code를 조립해 호출
        return (
            f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/{self.name}/callback"
            f"?code=mock:{state}"
        )

    async def exchange_code(self, code: str) -> OAuthUserInfo:
        if not code.startswith("mock:") or len(code) <= 5:
            raise ValueError("mock code 형식이 아닙니다")
        return OAuthUserInfo(provider=self.name, provider_user_id=code[5:])

    async def unlink(self, provider_user_id: str) -> None:
        return None


class KakaoProvider:
    """카카오 REST API. 실검증은 키 발급 후 (docs/api.md 참조)."""

    name = "kakao"
    _AUTH = "https://kauth.kakao.com/oauth/authorize"
    _TOKEN = "https://kauth.kakao.com/oauth/token"
    _ME = "https://kapi.kakao.com/v2/user/me"
    _UNLINK = "https://kapi.kakao.com/v1/user/unlink"

    @property
    def _redirect_uri(self) -> str:
        return f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/kakao/callback"

    def authorize_url(self, state: str) -> str:
        return (
            f"{self._AUTH}?response_type=code&client_id={settings.KAKAO_CLIENT_ID}"
            f"&redirect_uri={self._redirect_uri}&state={state}"
        )

    async def exchange_code(self, code: str) -> OAuthUserInfo:
        async with httpx.AsyncClient(timeout=10) as http:
            token_resp = await http.post(self._TOKEN, data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_CLIENT_ID,
                "client_secret": settings.KAKAO_CLIENT_SECRET or "",
                "redirect_uri": self._redirect_uri,
                "code": code,
            })
            token_resp.raise_for_status()
            access = token_resp.json()["access_token"]
            me = await http.get(self._ME, headers={"Authorization": f"Bearer {access}"})
            me.raise_for_status()
            return OAuthUserInfo(provider=self.name, provider_user_id=str(me.json()["id"]))

    async def unlink(self, provider_user_id: str) -> None:
        # admin 키 기반 unlink는 카카오 앱 설정 후 활성화. 실패해도 탈퇴는 진행.
        return None


class GoogleProvider:
    """구글 OAuth 2.0. 실검증은 키 발급 후."""

    name = "google"
    _AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
    _TOKEN = "https://oauth2.googleapis.com/token"
    _ME = "https://www.googleapis.com/oauth2/v2/userinfo"

    @property
    def _redirect_uri(self) -> str:
        return f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/google/callback"

    def authorize_url(self, state: str) -> str:
        return (
            f"{self._AUTH}?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self._redirect_uri}&scope=openid&state={state}"
        )

    async def exchange_code(self, code: str) -> OAuthUserInfo:
        async with httpx.AsyncClient(timeout=10) as http:
            token_resp = await http.post(self._TOKEN, data={
                "grant_type": "authorization_code",
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET or "",
                "redirect_uri": self._redirect_uri,
                "code": code,
            })
            token_resp.raise_for_status()
            access = token_resp.json()["access_token"]
            me = await http.get(self._ME, headers={"Authorization": f"Bearer {access}"})
            me.raise_for_status()
            return OAuthUserInfo(provider=self.name, provider_user_id=str(me.json()["id"]))

    async def unlink(self, provider_user_id: str) -> None:
        return None


_SUPPORTED = {"kakao", "google", "mock"}


def get_provider(name: str) -> OAuthProvider:
    if name not in _SUPPORTED:
        raise HTTPException(status_code=404, detail="지원하지 않는 로그인 제공자입니다")
    if settings.OAUTH_MOCK:
        return MockProvider(name)
    if name == "kakao":
        return KakaoProvider()
    if name == "google":
        return GoogleProvider()
    raise HTTPException(status_code=404, detail="지원하지 않는 로그인 제공자입니다")
