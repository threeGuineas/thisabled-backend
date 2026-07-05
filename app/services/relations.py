"""친구·차단 관계 판정 공용 (FRIEND · BLOCK-01). posts 피드, chat, 추천이 사용."""

import uuid

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestStatus
from app.core.pairs import normalize_pair
from app.models import Block, FriendRequest, Friendship


async def are_friends(db: AsyncSession, a: uuid.UUID, b: uuid.UUID) -> bool:
    ua, ub = normalize_pair(a, b)
    row = (
        await db.execute(
            select(Friendship.user_a).where(Friendship.user_a == ua, Friendship.user_b == ub)
        )
    ).scalar_one_or_none()
    return row is not None


async def is_blocked_either(db: AsyncSession, a: uuid.UUID, b: uuid.UUID) -> bool:
    """어느 방향이든 차단이면 True — 모든 접점 상호 제거 (BLOCK-01)."""
    row = (
        await db.execute(
            select(Block.blocker_id).where(
                or_(
                    (Block.blocker_id == a) & (Block.blocked_id == b),
                    (Block.blocker_id == b) & (Block.blocked_id == a),
                )
            )
        )
    ).first()
    return row is not None


async def block_user(db: AsyncSession, blocker: uuid.UUID, blocked: uuid.UUID) -> None:
    """차단: 친구 해제 + 진행 중 친구 요청 취소 + 차단 행 추가 (BLOCK-01)."""
    ua, ub = normalize_pair(blocker, blocked)
    await db.execute(
        delete(Friendship).where(Friendship.user_a == ua, Friendship.user_b == ub)
    )
    # 양방향 pending 요청은 흔적 없이 제거 (거절 이력과 달리 추천 제외에 쓰지 않음)
    await db.execute(
        delete(FriendRequest).where(
            or_(
                (FriendRequest.sender_id == blocker) & (FriendRequest.receiver_id == blocked),
                (FriendRequest.sender_id == blocked) & (FriendRequest.receiver_id == blocker),
            ),
            FriendRequest.status == RequestStatus.pending.value,
        )
    )
    db.add(Block(blocker_id=blocker, blocked_id=blocked))
