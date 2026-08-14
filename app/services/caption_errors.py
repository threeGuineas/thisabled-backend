"""CAPTION-01 실패 코드와 프론트 표시용 안전한 메시지."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CaptionFailureDetails:
    message: str
    retryable: bool


CAPTION_FAILURES: dict[str, CaptionFailureDetails] = {
    "CAPTION_SOURCE_MISSING": CaptionFailureDetails(
        "원본 영상을 찾을 수 없어 자막을 만들지 못했습니다.", False
    ),
    "CAPTION_PROCESSOR_UNAVAILABLE": CaptionFailureDetails(
        "자막 처리기를 사용할 수 없습니다. 잠시 후 다시 시도해 주세요.", True
    ),
    "CAPTION_AUDIO_EXTRACTION_FAILED": CaptionFailureDetails(
        "영상에서 음성을 추출하지 못했습니다. 자막 없이 게시할 수 있습니다.", False
    ),
    "CAPTION_CONFIGURATION_ERROR": CaptionFailureDetails(
        "자막 서비스 설정 오류가 발생했습니다. 관리자에게 문의해 주세요.", False
    ),
    "CAPTION_RESPONSE_INVALID": CaptionFailureDetails(
        "자막 응답을 처리하지 못했습니다. 관리자에게 문의해 주세요.", False
    ),
    "CAPTION_TRANSCRIPTION_FAILED": CaptionFailureDetails(
        "자막 생성에 실패했습니다. 잠시 후 다시 시도해 주세요.", True
    ),
    "CAPTION_GENERATION_FAILED": CaptionFailureDetails(
        "자막 생성에 실패했습니다. 다시 시도하거나 자막 없이 게시해 주세요.", True
    ),
}

DEFAULT_CAPTION_FAILURE_CODE = "CAPTION_GENERATION_FAILED"


class CaptionTranscriptionError(RuntimeError):
    """호출자가 자동 재시도 여부를 판단할 수 있는 자막 처리 오류."""

    def __init__(
        self, code: str, *, auto_retryable: bool, external_call_made: bool = False
    ):
        self.code = code
        self.auto_retryable = auto_retryable
        self.external_call_made = external_call_made
        super().__init__(code)


def caption_failure_details(code: str | None) -> CaptionFailureDetails | None:
    if code is None:
        return None
    return CAPTION_FAILURES.get(code, CAPTION_FAILURES[DEFAULT_CAPTION_FAILURE_CODE])


def caption_failure_state(
    status: str, code: str | None
) -> tuple[str | None, str | None, bool]:
    """failed 상태에만 안정적인 코드·표시 문구·재시도 가능 여부를 노출한다."""
    if status != "failed":
        return None, None, False
    resolved_code = (
        code if code in CAPTION_FAILURES else DEFAULT_CAPTION_FAILURE_CODE
    )
    details = caption_failure_details(resolved_code)
    assert details is not None
    return resolved_code, details.message, details.retryable
