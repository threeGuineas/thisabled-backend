"""v2.2 도메인 enum. DB에는 String으로 저장한다 (PG enum 마이그레이션 부담 회피)."""

from enum import StrEnum


class UiMode(StrEnum):
    """§5.2·GEN-01 — 가입 시 4종 중 하나 필수 선택."""

    visual = "visual"
    hearing = "hearing"
    developmental = "developmental"
    default = "default"


class PostStatus(StrEnum):
    """§POST-01 — '작성 중'은 서버 레코드 이전 단계라 상태로 두지 않음."""

    processing = "processing"
    published = "published"


class MediaType(StrEnum):
    image = "image"
    video = "video"


class AiStatus(StrEnum):
    """description_status / caption_status 공용."""

    none = "none"
    processing = "processing"
    done = "done"
    failed = "failed"


class SafetyStatus(StrEnum):
    """§SAFE — pending=분석 대기(비친구 보류), unanalyzed=성능저하 모드 미분석(§18.3)."""

    pending = "pending"
    safe = "safe"
    flagged = "flagged"
    unanalyzed = "unanalyzed"


class RoomState(StrEnum):
    """§CHAT-02 — request=요청함, active=일반 채팅."""

    request = "request"
    active = "active"


class RequestStatus(StrEnum):
    """friend_requests. declined+responded_at은 30일 추천 제외 근거(MATCH-03)."""

    pending = "pending"
    accepted = "accepted"
    declined = "declined"
    cancelled = "cancelled"


class MessageType(StrEnum):
    text = "text"
    image = "image"
    video = "video"


class Provider(StrEnum):
    kakao = "kakao"
    google = "google"
    mock = "mock"
