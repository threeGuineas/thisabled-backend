from pydantic import BaseModel


class STTResponse(BaseModel):
    text: str
    duration_ms: int
