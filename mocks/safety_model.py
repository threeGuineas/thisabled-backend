"""safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이.

계약: POST /analyze {text, receiver_is_minor} → {"verdict": "safe"|"flagged"}
데모용 규칙 기반. 실모델 교체 시 이 계약만 유지하면 백엔드 수정 불필요.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="safety-model (mock)")

# SAFE-02 탐지 유형 데모: 금전 요구·사기 / 성적 접근·만남 강요 / 괴롭힘·협박
_FLAG_WORDS = ["돈", "계좌", "송금", "만나자", "사진 보내", "비밀", "죽여", "협박"]
# §4.5: 미성년 수신자는 민감 임계값 — 추가 트리거
_MINOR_EXTRA = ["몇 살", "학교", "집 주소"]


class AnalyzeIn(BaseModel):
    text: str
    receiver_is_minor: bool = False


@app.post("/analyze")
async def analyze(body: AnalyzeIn):
    words = _FLAG_WORDS + (_MINOR_EXTRA if body.receiver_is_minor else [])
    verdict = "flagged" if any(w in body.text for w in words) else "safe"
    return {"verdict": verdict}


@app.get("/health")
async def health():
    return {"ok": True}
