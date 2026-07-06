"""MATCH — 후보 풀·제외 조건은 백엔드가 강제하고, 점수·사유만 모델 서버에 위임.

제외(MATCH-03·02-5): 자신 / 이미 친구 / 차단(양방향) / 거절 후 30일 미경과(양방향) /
미성년↔성인 상호. UI 모드는 서버 내부 특성으로만 전송하고 사유에 노출하지 않는다(MATCH-04).
"""

import uuid
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.age import age_band, is_minor
from app.core.config import settings
from app.core.enums import RequestStatus
from app.models import Block, FriendRequest, Friendship, InterestTag, User, UserInterestTag

DECLINE_EXCLUDE_DAYS = 30  # MATCH-03

# MATCH-04: 추천 사유에 장애·모드 관련 표현 금지 — 응답 검증 필터
_FORBIDDEN_REASON_WORDS = ("장애", "모드", "시각", "청각", "발달")


class MatchUnavailable(Exception):
    pass


class MatchClient:
    async def score(self, me_features: dict, candidates: list[dict]) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as http:
                resp = await http.post(
                    f"{settings.MATCH_MODEL_URL}/score",
                    json={"me": me_features, "candidates": candidates},
                )
                resp.raise_for_status()
                return resp.json()["results"]
        except httpx.HTTPError as exc:
            raise MatchUnavailable() from exc


def get_match_client() -> MatchClient:
    """FastAPI 의존성 — 테스트에서 fake로 override."""
    return MatchClient()


def sanitize_reasons(reasons: list[str]) -> list[str]:
    return [r for r in reasons if not any(w in r for w in _FORBIDDEN_REASON_WORDS)]


async def candidate_pool(db: AsyncSession, me: User) -> list[User]:
    friend_rows = (
        await db.execute(
            select(Friendship).where(or_(Friendship.user_a == me.id, Friendship.user_b == me.id))
        )
    ).scalars().all()
    friend_ids = {f.user_b if f.user_a == me.id else f.user_a for f in friend_rows}

    block_rows = (
        await db.execute(
            select(Block).where(or_(Block.blocker_id == me.id, Block.blocked_id == me.id))
        )
    ).scalars().all()
    blocked_ids = {b.blocked_id if b.blocker_id == me.id else b.blocker_id for b in block_rows}

    decline_cutoff = datetime.now(timezone.utc) - timedelta(days=DECLINE_EXCLUDE_DAYS)
    declined_rows = (
        await db.execute(
            select(FriendRequest).where(
                FriendRequest.status == RequestStatus.declined.value,
                FriendRequest.responded_at > decline_cutoff,
                or_(FriendRequest.sender_id == me.id, FriendRequest.receiver_id == me.id),
            )
        )
    ).scalars().all()
    declined_ids = {
        r.receiver_id if r.sender_id == me.id else r.sender_id for r in declined_rows
    }

    excluded = friend_ids | blocked_ids | declined_ids | {me.id}
    users = (
        await db.execute(select(User).where(User.id.not_in(excluded)))
    ).scalars().all()

    # §4.5: 미성년↔성인 상호 추천 제외
    me_minor = is_minor(me.birth_date)
    return [u for u in users if is_minor(u.birth_date) == me_minor]


async def user_features(db: AsyncSession, user: User) -> dict:
    """모델 입력 특성. 생년월일 원문 대신 연령대만 (MATCH-02-5)."""
    tag_codes = (
        await db.execute(
            select(InterestTag.code)
            .join(UserInterestTag, UserInterestTag.tag_id == InterestTag.id)
            .where(UserInterestTag.user_id == user.id)
        )
    ).scalars().all()
    return {
        "user_id": str(user.id),
        "bio": user.bio or "",
        "tags": list(tag_codes),
        "age_band": age_band(user.birth_date),
        "ui_mode": user.ui_mode,  # 서버 내부 특성 — 사유·응답에 노출 금지 (MATCH-04)
    }
