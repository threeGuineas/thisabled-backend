import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    content: str = Field(examples=["오늘 산책하면서 찍은 사진이에요 🌳"])
    image_url: str | None = Field(
        default=None,
        description="선택. POST /upload 응답 url(/uploads/...)을 그대로 사용.",
        examples=["/uploads/3f2a....png"],
    )


class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    image_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
