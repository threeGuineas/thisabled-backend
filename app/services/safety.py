"""SAFE-01 — 자체 안전 모델 HTTP 클라이언트 (별도 모델 서버 경계, AI 팀 담당).

텍스트 위험 판정에는 외부 AI를 사용하지 않는다 (§17.1).
타임아웃(기본 2초)·5xx는 SafetyUnavailable → §18.3 성능저하 모드로 처리한다.
"""

import httpx

from app.core.config import settings


class SafetyUnavailable(Exception):
    """모델 서버 장애·지연 — 친구 텍스트는 unanalyzed 전달, 비친구는 pending 보류."""


class SafetyClient:
    async def analyze(self, text: str, *, receiver_is_minor: bool) -> str:
        """→ 'safe' | 'flagged'. 미성년 수신자는 민감(낮은) 임계값 (§4.5)."""
        try:
            async with httpx.AsyncClient(timeout=settings.SAFETY_TIMEOUT_SECONDS) as http:
                resp = await http.post(
                    f"{settings.SAFETY_MODEL_URL}/analyze",
                    json={"text": text, "receiver_is_minor": receiver_is_minor},
                )
                resp.raise_for_status()
                verdict = resp.json().get("verdict")
        except httpx.HTTPError as exc:
            raise SafetyUnavailable() from exc
        if verdict not in ("safe", "flagged"):
            raise SafetyUnavailable()
        return verdict


def get_safety_client() -> SafetyClient:
    """FastAPI 의존성 — 테스트에서 fake로 override."""
    return SafetyClient()
