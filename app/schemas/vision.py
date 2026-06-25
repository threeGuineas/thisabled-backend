from pydantic import BaseModel, Field


class VisionRequest(BaseModel):
    image_url: str = Field(
        description="우리 업로드 경로(/uploads/<uuid>.ext)만 허용. 외부 URL 불가.",
        examples=["/uploads/3f2a1b9c-....png"],
    )


class VisionResponse(BaseModel):
    description: str = Field(description="이미지의 한국어 설명")
    duration_ms: int = Field(description="생성 소요(ms). 캐시 적중 시 0.")
    cached: bool = Field(description="true면 24h 캐시에서 반환(API 미호출).")
