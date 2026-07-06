"""BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models import Block, User
from app.schemas.post import AuthorOut
from app.schemas.social import BlockIn, BlockListOut
from app.services.relations import block_user

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.post("", status_code=201)
async def create_block(
    body: BlockIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.user_id == user.id:
        raise HTTPException(status_code=400, detail="자기 자신은 차단할 수 없습니다")
    target = await db.get(User, body.user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    exists = await db.get(Block, (user.id, body.user_id))
    if exists is None:
        await block_user(db, user.id, body.user_id)
        await db.commit()
    return {"blocked": True}


@router.delete("/{user_id}", status_code=204)
async def remove_block(
    user_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(
        delete(Block).where(Block.blocker_id == user.id, Block.blocked_id == user_id)
    )
    await db.commit()


@router.get("", response_model=BlockListOut)
async def list_blocks(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            select(User)
            .join(Block, Block.blocked_id == User.id)
            .where(Block.blocker_id == user.id)
        )
    ).scalars().all()
    return BlockListOut(
        items=[AuthorOut(id=u.id, nickname=u.nickname, profile_image_url=u.profile_image_url) for u in rows]
    )
