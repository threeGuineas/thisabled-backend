from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.modes import settings_for
from app.db.session import get_db
from app.models.user import User, UserModeHistory
from app.schemas.mode import ModeResponse, ModeUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me/mode",
    response_model=ModeResponse,
    summary="현재 장애 모드 조회",
    description="미설정(온보딩 전)이면 `default`로 응답. `settings`는 모드별 UI 기본값(폰트·자막·해설 토글 등).",
)
async def get_mode(current_user: User = Depends(get_current_user)):
    mode = current_user.disability_mode or "default"
    return ModeResponse(mode=mode, settings=settings_for(mode, current_user.mode_settings))


@router.put(
    "/me/mode",
    response_model=ModeResponse,
    summary="장애 모드 변경",
    description="`visual` · `hearing` · `developmental` · `default` 중 하나. 변경 시 이력(user_mode_history)이 기록된다.",
)
async def update_mode(
    body: ModeUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_mode = body.mode.value
    from_mode = current_user.disability_mode

    if from_mode != new_mode:
        db.add(UserModeHistory(user_id=current_user.id, from_mode=from_mode, to_mode=new_mode))
        current_user.disability_mode = new_mode
        await db.commit()
        await db.refresh(current_user)

    return ModeResponse(
        mode=new_mode,
        settings=settings_for(new_mode, current_user.mode_settings),
        changed_at=datetime.now(timezone.utc),
    )
