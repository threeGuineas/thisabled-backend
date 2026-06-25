from datetime import datetime

from pydantic import BaseModel

from app.core.modes import DisabilityMode


class ModeUpdateRequest(BaseModel):
    mode: DisabilityMode


class ModeResponse(BaseModel):
    mode: str
    settings: dict
    changed_at: datetime | None = None
