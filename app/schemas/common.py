"""API 요청 DTO의 공통 검증 정책."""

from pydantic import BaseModel, ConfigDict


class StrictRequest(BaseModel):
    """프론트 필드 오타를 조용히 무시하지 않고 422로 드러낸다."""

    model_config = ConfigDict(extra="forbid")
