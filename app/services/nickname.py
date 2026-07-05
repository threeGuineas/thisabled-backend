"""닉네임 정책 (ACC-01): 2~12자 한글·영문·숫자, 금칙어·중복 불가."""

import re

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ForbiddenNickname, User

_NICKNAME_RE = re.compile(r"^[가-힣a-zA-Z0-9]{2,12}$")


async def validate_nickname(db: AsyncSession, nickname: str, *, exclude_user_id=None) -> None:
    """형식(400) → 금칙어(400) → 중복(409) 순 검증. 통과 시 None."""
    if not _NICKNAME_RE.fullmatch(nickname):
        raise HTTPException(status_code=400, detail="닉네임은 2~12자 한글·영문·숫자만 가능합니다")

    words = (await db.execute(select(ForbiddenNickname.word))).scalars().all()
    lowered = nickname.lower()
    if any(w.lower() in lowered for w in words):
        raise HTTPException(status_code=400, detail="사용할 수 없는 닉네임입니다")

    q = select(User.id).where(User.nickname == nickname)
    if exclude_user_id is not None:
        q = q.where(User.id != exclude_user_id)
    if (await db.execute(q)).scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="이미 사용 중인 닉네임입니다")
