"""§16 알림 목록·읽음 처리."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models import Notification, User

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationOut(BaseModel):
    id: uuid.UUID
    type: str
    payload: dict
    read_at: datetime | None
    created_at: datetime


class NotificationListOut(BaseModel):
    items: list[NotificationOut]


class ReadIn(BaseModel):
    ids: list[uuid.UUID]


@router.get("", response_model=NotificationListOut)
async def list_notifications(
    limit: int = Query(default=50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            select(Notification)
            .where(Notification.user_id == user.id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
    ).scalars().all()
    return NotificationListOut(
        items=[
            NotificationOut(
                id=n.id, type=n.type, payload=n.payload, read_at=n.read_at, created_at=n.created_at
            )
            for n in rows
        ]
    )


@router.post("/read")
async def mark_read(
    body: ReadIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(
        update(Notification)
        .where(
            Notification.user_id == user.id,
            Notification.id.in_(body.ids),
            Notification.read_at.is_(None),
        )
        .values(read_at=datetime.now(timezone.utc))
    )
    await db.commit()
    return {"read": True}
