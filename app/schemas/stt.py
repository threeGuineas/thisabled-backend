from pydantic import BaseModel, Field


class STTResponse(BaseModel):
    text: str = Field(description="전사된 한국어 텍스트")
    duration_ms: int = Field(description="전사 소요(ms)")
