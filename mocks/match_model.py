"""match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이.

계약: POST /score {me, candidates:[{user_id, bio, tags, age_band, ui_mode}]}
      → {"results": [{user_id, score, reasons}]}
데모용: 관심사 교집합 + 연령대 일치 기반 단순 점수. 사유는 일반화 문장만 (MATCH-04).
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="match-model (mock)")


class Features(BaseModel):
    user_id: str
    bio: str = ""
    tags: list[str] = []
    age_band: str = ""
    ui_mode: str = ""


class ScoreIn(BaseModel):
    me: Features
    candidates: list[Features]


@app.post("/score")
async def score(body: ScoreIn):
    results = []
    my_tags = set(body.me.tags)
    for c in body.candidates:
        overlap = len(my_tags & set(c.tags))
        s = min(0.3 + overlap * 0.15 + (0.1 if c.age_band == body.me.age_band else 0.0), 1.0)
        reasons = []
        if overlap:
            reasons.append("관심사가 비슷해요")
        if c.age_band == body.me.age_band:
            reasons.append("비슷한 연령대예요")
        if not reasons:
            reasons.append("새로운 친구를 만나보세요")
        results.append({"user_id": c.user_id, "score": round(s, 2), "reasons": reasons})
    return {"results": results}


@app.get("/health")
async def health():
    return {"ok": True}
