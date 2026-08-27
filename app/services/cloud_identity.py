"""Cloud Run 서비스 간 호출용 Google 발급 ID 토큰."""

import asyncio
import time

import jwt
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token

_tokens: dict[str, tuple[str, float]] = {}
_lock = asyncio.Lock()


class CloudIdentityError(RuntimeError):
    pass


def _fetch(audience: str) -> tuple[str, float]:
    try:
        token = fetch_id_token(Request(), audience)
        claims = jwt.decode(token, options={"verify_signature": False})
        return token, float(claims["exp"])
    except Exception as exc:  # metadata/ADC 장애를 도메인 오류로 정규화
        raise CloudIdentityError("Cloud Run ID token 발급에 실패했습니다") from exc


async def service_auth_headers(audience: str | None) -> dict[str, str]:
    """audience 미설정(로컬/compose)이면 인증 헤더 없이 호출한다."""
    if not audience:
        return {}
    cached = _tokens.get(audience)
    if cached is not None and cached[1] - 60 > time.time():
        return {"Authorization": f"Bearer {cached[0]}"}

    async with _lock:
        cached = _tokens.get(audience)
        if cached is None or cached[1] - 60 <= time.time():
            _tokens[audience] = await asyncio.to_thread(_fetch, audience)
        return {"Authorization": f"Bearer {_tokens[audience][0]}"}
