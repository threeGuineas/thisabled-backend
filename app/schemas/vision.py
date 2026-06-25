from pydantic import BaseModel


class VisionRequest(BaseModel):
    image_url: str  # 우리 업로드 경로: /uploads/<uuid>.ext


class VisionResponse(BaseModel):
    description: str
    duration_ms: int
    cached: bool
