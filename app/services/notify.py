"""§16 알림 생성 — DB 저장 + WS 푸시 병행. 표현(시각·음성·진동)은 FE가 모드별 처리."""

import uuid

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Notification
from app.services.events import publish_to_user

# §16 알림 유형
FRIEND_REQUEST = "friend.request"
FRIEND_ACCEPTED = "friend.accepted"
POST_COMMENT = "post.comment"
POST_LIKE = "post.like"
POST_PUBLISHED = "post.published"
CHAT_REQUEST = "chat.request"
CHAT_FLAGGED = "chat.flagged"  # 주의 메시지 도착 (수신자 대상)
CHAT_RESTRICTED = "chat.restricted"  # SAFE-05-5 수신자 안내
CAPTION_DONE = "media.caption_done"
CAPTION_FAILED = "media.caption_failed"
DESCRIPTION_DONE = "media.description_done"
DESCRIPTION_FAILED = "media.description_failed"


async def notify(
    db: AsyncSession, redis: aioredis.Redis, user_id, type_: str, payload: dict
) -> None:
    db.add(Notification(id=uuid.uuid4(), user_id=user_id, type=type_, payload=payload))
    await db.commit()
    await publish_to_user(redis, user_id, {"type": "notification", "payload": {"type": type_, **payload}})
