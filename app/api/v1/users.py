"""ACC-03 프로필 · TAG-01 태그 · §15 설정 · §5.2 모드 변경."""

import re
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.age import is_minor
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models import InterestTag, User, UserInterestTag, UserModeHistory
from app.schemas.user import (
    MeOut,
    ModePutIn,
    ProfilePatchIn,
    PublicProfileOut,
    SettingsPatchIn,
    TagCatalogOut,
    TagOut,
    TagsPutIn,
    WithdrawIn,
)
from app.services.nickname import validate_nickname
from app.services.relations import is_blocked_either
from app.services.withdrawal import withdraw

router = APIRouter(tags=["users"])

MAX_TAGS = 10  # TAG-01

# MATCH-02-7: 자기소개 연락처 입력 방지 — 전화번호 / 이메일 / 외부 메신저 ID 유도
_CONTACT_PATTERNS = [
    re.compile(r"01[016789][ -.]?\d{3,4}[ -.]?\d{4}"),
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    re.compile(r"(카톡|카카오톡|kakao|텔레그램|telegram|인스타|insta)\s*(id|아이디|ID)?\s*[:：]?\s*\w+", re.IGNORECASE),
]


def _reject_contact_in_bio(bio: str) -> None:
    for pattern in _CONTACT_PATTERNS:
        if pattern.search(bio):
            raise HTTPException(
                status_code=400, detail="자기소개에 연락처를 쓸 수 없습니다. 삭제 후 다시 시도해 주세요"
            )


async def _user_tags(db: AsyncSession, user_id: uuid.UUID) -> list[TagOut]:
    rows = (
        await db.execute(
            select(InterestTag)
            .join(UserInterestTag, UserInterestTag.tag_id == InterestTag.id)
            .where(UserInterestTag.user_id == user_id)
        )
    ).scalars().all()
    return [TagOut(code=t.code, category=t.category, label=t.label) for t in rows]


def _me_out(user: User, tags: list[TagOut]) -> MeOut:
    return MeOut(
        id=user.id,
        nickname=user.nickname,
        bio=user.bio,
        profile_image_url=user.profile_image_url,
        ui_mode=user.ui_mode,
        is_minor=is_minor(user.birth_date),
        stranger_requests_allowed=user.stranger_requests_allowed,
        mode_settings=user.mode_settings,
        tags=tags,
    )


@router.get("/tags", response_model=TagCatalogOut)
async def tag_catalog(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(InterestTag).order_by(InterestTag.category))).scalars().all()
    return TagCatalogOut(tags=[TagOut(code=t.code, category=t.category, label=t.label) for t in rows])


@router.get("/users/me", response_model=MeOut)
async def me(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return _me_out(user, await _user_tags(db, user.id))


@router.patch("/users/me", response_model=MeOut)
async def patch_me(
    body: ProfilePatchIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.nickname is not None and body.nickname != user.nickname:
        await validate_nickname(db, body.nickname, exclude_user_id=user.id)
        user.nickname = body.nickname
    if body.bio is not None:
        _reject_contact_in_bio(body.bio)
        user.bio = body.bio
    if body.profile_image_url is not None:
        user.profile_image_url = body.profile_image_url
    await db.commit()
    return _me_out(user, await _user_tags(db, user.id))


@router.put("/users/me/tags", response_model=MeOut)
async def put_tags(
    body: TagsPutIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    codes = list(dict.fromkeys(body.tag_codes))  # 중복 제거, 순서 유지
    if len(codes) > MAX_TAGS:
        raise HTTPException(status_code=400, detail=f"관심사 태그는 최대 {MAX_TAGS}개까지 선택할 수 있습니다")
    tags = (
        (await db.execute(select(InterestTag).where(InterestTag.code.in_(codes)))).scalars().all()
        if codes
        else []
    )
    if len(tags) != len(codes):
        raise HTTPException(status_code=404, detail="존재하지 않는 태그가 있습니다")
    await db.execute(delete(UserInterestTag).where(UserInterestTag.user_id == user.id))
    for tag in tags:
        db.add(UserInterestTag(user_id=user.id, tag_id=tag.id))
    await db.commit()
    return _me_out(user, await _user_tags(db, user.id))


@router.patch("/users/me/settings", response_model=MeOut)
async def patch_settings(
    body: SettingsPatchIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.stranger_requests_allowed is not None:
        user.stranger_requests_allowed = body.stranger_requests_allowed
    if body.mode_settings is not None:
        user.mode_settings = body.mode_settings
    await db.commit()
    return _me_out(user, await _user_tags(db, user.id))


@router.put("/users/me/mode", response_model=MeOut)
async def put_mode(
    body: ModePutIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.ui_mode.value != user.ui_mode:
        db.add(
            UserModeHistory(
                id=uuid.uuid4(),
                user_id=user.id,
                from_mode=user.ui_mode,
                to_mode=body.ui_mode.value,
            )
        )
        user.ui_mode = body.ui_mode.value
        await db.commit()
    return _me_out(user, await _user_tags(db, user.id))


@router.delete("/users/me", status_code=204)
async def withdraw_me(
    body: WithdrawIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """§15 회원 탈퇴. 게시물·댓글 처리는 사용자가 선택(탈퇴 화면 확인 단계는 FE)."""
    await withdraw(db, user, body.posts_action)


@router.get("/users/{user_id}", response_model=PublicProfileOut)
async def public_profile(
    user_id: uuid.UUID,
    viewer: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    target = await db.get(User, user_id)
    # 차단 관계는 존재 자체를 숨긴다 (BLOCK-01)
    if target is None or await is_blocked_either(db, viewer.id, user_id):
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return PublicProfileOut(
        id=target.id,
        nickname=target.nickname,
        bio=target.bio,
        profile_image_url=target.profile_image_url,
        tags=await _user_tags(db, target.id),
    )
