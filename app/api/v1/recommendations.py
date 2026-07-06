"""MATCH — 맞춤 친구 추천."""

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.services.match import (
    MatchUnavailable,
    candidate_pool,
    get_match_client,
    sanitize_reasons,
    user_features,
)

router = APIRouter(tags=["recommendations"])

NOT_ENOUGH = "추천 정보가 부족합니다"  # MATCH-02-8
TEMPORARY = "지금은 추천을 만들 수 없어요. 잠시 후 다시 시도해 주세요"  # §18.3


class RecommendationOut(BaseModel):
    user_id: uuid.UUID
    nickname: str
    bio: str | None
    profile_image_url: str | None
    tags: list[str]  # 태그 코드 — 상세는 프로필 조회(GET /users/{id})
    score: float
    reasons: list[str]


class RecommendationListOut(BaseModel):
    items: list[RecommendationOut]
    message: str | None = None


@router.get("/recommendations", response_model=RecommendationListOut)
async def recommendations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    match_client=Depends(get_match_client),
):
    pool = await candidate_pool(db, user)
    if not pool:
        return RecommendationListOut(items=[], message=NOT_ENOUGH)

    me_features = await user_features(db, user)
    candidates = [await user_features(db, c) for c in pool]
    try:
        results = await match_client.score(me_features, candidates)
    except MatchUnavailable:
        return RecommendationListOut(items=[], message=TEMPORARY)

    by_id = {str(u.id): u for u in pool}
    items: list[RecommendationOut] = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        candidate = by_id.get(str(r["user_id"]))
        if candidate is None:
            continue
        cand_features = next(c for c in candidates if c["user_id"] == str(candidate.id))
        items.append(
            RecommendationOut(
                user_id=candidate.id,
                nickname=candidate.nickname,
                bio=candidate.bio,
                profile_image_url=candidate.profile_image_url,
                tags=cand_features["tags"],
                score=r["score"],
                reasons=sanitize_reasons(r.get("reasons", [])),
            )
        )
    if not items:
        return RecommendationListOut(items=[], message=NOT_ENOUGH)
    return RecommendationListOut(items=items)
