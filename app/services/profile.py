"""프로필 화면용 활동 집계와 친구 관계 projection."""

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import PostStatus, RequestStatus
from app.models import Comment, FriendRequest, Post, PostLike
from app.schemas.user import ProfileRelationshipOut, ProfileStatsOut
from app.services.relations import are_friends


async def activity_stats(db: AsyncSession, user_id: uuid.UUID) -> ProfileStatsOut:
    """화면의 게시글·댓글·좋아요 수를 명시된 의미로 한 번에 계산한다."""
    post_count = (
        select(func.count()).select_from(Post).where(
            Post.author_id == user_id,
            Post.status == PostStatus.published.value,
        )
    ).scalar_subquery()
    comment_count = (
        select(func.count()).select_from(Comment).where(Comment.author_id == user_id)
    ).scalar_subquery()
    received_like_count = (
        select(func.count())
        .select_from(PostLike)
        .join(Post, Post.id == PostLike.post_id)
        .where(
            Post.author_id == user_id,
            Post.status == PostStatus.published.value,
        )
    ).scalar_subquery()
    counts = (await db.execute(select(post_count, comment_count, received_like_count))).one()
    return ProfileStatsOut(
        post_count=counts[0],
        comment_count=counts[1],
        received_like_count=counts[2],
    )


async def relationship(
    db: AsyncSession, viewer_id: uuid.UUID, target_id: uuid.UUID
) -> ProfileRelationshipOut:
    if viewer_id == target_id:
        return ProfileRelationshipOut(status="self")
    if await are_friends(db, viewer_id, target_id):
        return ProfileRelationshipOut(status="friends")
    pending = (
        await db.execute(
            select(FriendRequest).where(
                FriendRequest.status == RequestStatus.pending.value,
                or_(
                    (FriendRequest.sender_id == viewer_id)
                    & (FriendRequest.receiver_id == target_id),
                    (FriendRequest.sender_id == target_id)
                    & (FriendRequest.receiver_id == viewer_id),
                ),
            )
        )
    ).scalar_one_or_none()
    if pending is None:
        return ProfileRelationshipOut(status="none")
    status = "request_sent" if pending.sender_id == viewer_id else "request_received"
    return ProfileRelationshipOut(status=status, request_id=pending.id)
