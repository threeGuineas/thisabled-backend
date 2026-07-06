"""§15 회원 탈퇴.

- 계정·프로필 즉시 삭제 (users hard delete)
- 게시물·댓글: 사용자가 익명화/삭제 선택
- 채팅 메시지: 상대방 기록 보존을 위해 유지 + 발신자 익명화 (FK SET NULL)
- 좋아요·친구·요청·알림·전송제한·위험점수: 계정과 함께 삭제 (FK CASCADE / 행 삭제)
- 소셜 unlink + withdrawn_socials 기록 → 30일 재가입 제한
"""

import uuid
from typing import Literal

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Comment, Post, SocialIdentity, User, WithdrawnSocial
from app.services.oauth import get_provider

PostsAction = Literal["anonymize", "delete"]


async def withdraw(db: AsyncSession, user: User, posts_action: PostsAction) -> None:
    if posts_action == "delete":
        # 게시물 삭제 → media·comments·likes는 FK CASCADE
        await db.execute(delete(Post).where(Post.author_id == user.id))
        # 남의 글에 단 내 댓글도 함께 삭제
        await db.execute(delete(Comment).where(Comment.author_id == user.id))
    else:
        # '탈퇴한 사용자'로 익명화 유지
        await db.execute(update(Post).where(Post.author_id == user.id).values(author_id=None))
        await db.execute(
            update(Comment).where(Comment.author_id == user.id).values(author_id=None)
        )

    identities = (
        await db.execute(select(SocialIdentity).where(SocialIdentity.user_id == user.id))
    ).scalars().all()
    for identity in identities:
        # unlink 실패(제공자 장애)해도 탈퇴는 진행한다
        try:
            await get_provider(identity.provider).unlink(identity.provider_user_id)
        except Exception:
            pass
        db.add(
            WithdrawnSocial(
                id=uuid.uuid4(),
                provider=identity.provider,
                provider_user_id=identity.provider_user_id,
            )
        )

    # users 행 삭제 → chat_messages.sender_id·chat_rooms.user_x SET NULL(익명화),
    # 나머지(social_identities·tags·friendships·requests·blocks·notifications·
    # send_restrictions·mode_history·post_likes)는 CASCADE. risk_score도 행과 함께 소멸.
    await db.delete(user)
    await db.commit()
