"""COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상).

버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개 텍스트만 전송하며
flagged & 미열람 메시지는 제외한다. OPENAI_API_KEY가 없으면 stub이 고정 후보를 준다.
"""

import json

from openai import AsyncOpenAI

from app.core.config import settings

_SYSTEM = (
    "당신은 발달장애인을 포함한 사용자의 소통을 돕는 코치입니다. "
    "쉬운 한국어 문장으로, 상대를 공격하거나 유해한 표현 없이 제안하세요. "
    "상대방의 의도나 감정을 사실로 단정하지 마세요."
)


class StubCommClient:
    """키 미설정 dev/시연용 — 고정 후보."""

    async def simplify(self, text: str) -> str:
        return f"쉽게 말하면: {text[:50]}"

    async def complete(self, text: str) -> list[str]:
        return [f"{text} 좋아요.", f"{text} 어떠세요?"]

    async def suggest_replies(self, messages: list[str]) -> list[str]:
        return ["좋아요!", "고마워요", "다음에 또 이야기해요"]

    async def hints(self, messages: list[str]) -> list[str]:
        return ["인사로 시작해 보세요", "궁금한 점을 물어보세요", "부담되면 거절해도 괜찮아요"]


class OpenAICommClient:
    def __init__(self):
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def _ask(self, instruction: str, payload: str, want_list: bool):
        resp = await self._client.chat.completions.create(
            model=settings.VISION_MODEL,
            max_tokens=300,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": f"{instruction}\n\n{payload}"},
            ],
        )
        content = (resp.choices[0].message.content or "").strip()
        if not want_list:
            return content
        try:
            parsed = json.loads(content)
            return parsed if isinstance(parsed, list) else [content]
        except json.JSONDecodeError:
            return [line.strip("- ").strip() for line in content.splitlines() if line.strip()][:3]

    async def simplify(self, text: str) -> str:
        return await self._ask("다음 글을 쉬운 문장으로 바꿔주세요.", text, want_list=False)

    async def complete(self, text: str) -> list[str]:
        return await self._ask(
            "다음 미완성 문장의 완성본 후보 2개를 JSON 배열로 주세요.", text, want_list=True
        )

    async def suggest_replies(self, messages: list[str]) -> list[str]:
        return await self._ask(
            "다음 대화에 어울리는 답장 후보 3개를 JSON 배열로 주세요.",
            "\n".join(messages), want_list=True,
        )

    async def hints(self, messages: list[str]) -> list[str]:
        return await self._ask(
            "다음 대화 맥락에서 인사·질문·거절 등 소통 힌트 3개를 JSON 배열로 주세요.",
            "\n".join(messages), want_list=True,
        )


def get_comm_client():
    """FastAPI 의존성 — 테스트에서 fake로 override."""
    if settings.OPENAI_API_KEY:
        return OpenAICommClient()
    return StubCommClient()
