"""GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드).

엔드포인트는 `vision.generate_description(...)` 을 호출한다.
테스트는 이 함수를 monkeypatch 해서 실제 OpenAI 호출 없이 검증한다.
"""

import base64

from openai import AsyncOpenAI

from app.core.config import settings

_client: AsyncOpenAI | None = None

_SYSTEM_PROMPT = (
    "당신은 시각장애인 사용자를 위해 이미지를 음성으로 설명하는 화면 해설가입니다. "
    "이미지를 한국어로 50~150자 이내로, 핵심 사물·인물·상황·색감·분위기를 "
    "자연스러운 한 문단으로 묘사하세요. 추측하지 말고 보이는 것만 설명하세요."
)


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY 가 설정되지 않았습니다 (.env 확인)")
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def generate_description(image_bytes: bytes, content_type: str) -> str:
    """이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)"""
    b64 = base64.b64encode(image_bytes).decode()
    data_url = f"data:{content_type};base64,{b64}"

    resp = await _get_client().chat.completions.create(
        model=settings.VISION_MODEL,
        max_tokens=settings.VISION_MAX_TOKENS,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지를 설명해 주세요."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
    )
    return (resp.choices[0].message.content or "").strip()
