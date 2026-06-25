import uuid
from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str
    image_url: str | None = None


class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    image_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
