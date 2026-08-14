"""프론트엔드 구현자를 위한 OpenAPI 문서 보강.

FastAPI의 기본 스키마는 타입은 정확하지만 비즈니스 상태와 화면 처리 방법을
설명하지 않는다. 이 모듈은 런타임 라우팅을 건드리지 않고, 메서드+경로를 키로
모든 HTTP 작업의 설명·예시·오류 계약을 한곳에서 관리한다.
"""

from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


UUID_A = "11111111-1111-4111-8111-111111111111"
UUID_B = "22222222-2222-4222-8222-222222222222"


@dataclass(frozen=True)
class OperationGuide:
    summary: str
    description: str
    success: str
    success_status: str | None = None
    request_example: dict[str, Any] | None = None
    response_examples: dict[str, Any] = field(default_factory=dict)
    errors: dict[int, str] = field(default_factory=dict)
    remove_responses: tuple[str, ...] = ()


def _guide(
    summary: str,
    description: str,
    success: str,
    *,
    request: dict[str, Any] | None = None,
    examples: dict[str, Any] | None = None,
    errors: dict[int, str] | None = None,
    remove: tuple[str, ...] = (),
    status: str | None = None,
) -> OperationGuide:
    return OperationGuide(
        summary=summary,
        description=description,
        success=success,
        success_status=status,
        request_example=request,
        response_examples=examples or {},
        errors=errors or {},
        remove_responses=remove,
    )


# 문서 품질 테스트가 이 목록과 실제 HTTP 라우트를 1:1로 비교한다.
OPERATION_GUIDES: dict[tuple[str, str], OperationGuide] = {
    ("get", "/api/v1/health"): _guide(
        "서버 상태 확인",
        "DB와 Redis에 실제로 연결해 상태를 확인합니다. `status=ok`일 때만 서비스가 정상이며, "
        "`degraded`이면 프론트 기능 호출보다 점검 안내를 우선 표시하세요.",
        "DB·Redis가 모두 정상이면 200과 각 구성요소의 `ok` 상태를 반환합니다.",
        examples={"normal": {"summary": "정상", "value": {"status": "ok", "db": "ok", "redis": "ok"}}},
    ),
    ("get", "/api/v1/auth/{provider}/authorize"): _guide(
        "소셜 로그인 URL 발급",
        "`provider`는 `kakao`, `google`, 개발 환경의 `mock` 중 하나입니다. 반환된 URL로 브라우저를 "
        "이동시키고, 로그인 완료 후 callback이 프론트 주소로 다시 리다이렉트합니다.",
        "200 응답의 `authorize_url`을 브라우저 전체 이동에 사용합니다.",
        errors={404: "지원하지 않는 provider입니다."},
    ),
    ("get", "/api/v1/auth/{provider}/callback"): _guide(
        "소셜 로그인 콜백 처리",
        "OAuth 제공자가 호출하는 브라우저용 엔드포인트입니다. 프론트가 직접 JSON을 요청하지 않습니다. "
        "기가입자는 `is_new_user=false&access_token=...`, 신규는 `is_new_user=true&signup_token=...`, "
        "실패는 `error={provider}_failed` 쿼리를 붙여 `FRONTEND_URL`로 이동합니다.",
        "302로 프론트 SPA에 이동합니다. 기가입자 응답에는 refresh_token 쿠키도 설정됩니다.",
        errors={404: "지원하지 않는 provider입니다."},
        remove=("200",),
        status="302",
    ),
    ("post", "/api/v1/auth/signup"): _guide(
        "신규 회원가입 완료",
        "OAuth callback에서 받은 30분 유효 `signup_token`과 필수 프로필·약관 동의를 제출합니다. "
        "성공하면 access token을 저장하고, 응답의 `stranger_requests_allowed`로 초기 채팅 요청 UI를 설정하세요.",
        "201과 access token, 사용자 UUID, 비친구 요청 초기값을 반환하고 refresh_token 쿠키를 설정합니다.",
        request={
            "signup_token": "callback에서 받은 signup_token",
            "nickname": "새싹친구",
            "birth_date": "2000-05-20",
            "ui_mode": "developmental",
            "agreements": {"terms": True, "privacy": True, "ai_notice": True},
        },
        errors={
            400: "필수 약관 미동의, 만 14세 미만 또는 닉네임 정책 위반.",
            401: "signup_token이 만료되었거나 올바르지 않습니다.",
            403: "탈퇴 후 30일 재가입 제한 기간입니다.",
            409: "같은 소셜 계정으로 이미 가입되어 있습니다.",
        },
    ),
    ("post", "/api/v1/auth/refresh"): _guide(
        "Access token 재발급",
        "브라우저의 httpOnly `refresh_token` 쿠키를 사용합니다. 프론트 요청에는 반드시 credentials를 "
        "포함하고, access token 만료로 401을 받은 뒤 한 번만 재발급·재시도하세요.",
        "200과 새 access token을 반환합니다. refresh token은 응답 본문에 노출되지 않습니다.",
        errors={401: "쿠키 누락·만료·위조 또는 탈퇴한 사용자입니다."},
    ),
    ("post", "/api/v1/auth/logout"): _guide(
        "로그아웃",
        "서버의 refresh_token 쿠키를 삭제합니다. 프론트는 응답 성공 여부와 관계없이 메모리·로컬 저장소의 "
        "access token도 함께 제거하고 로그인 화면으로 이동하세요.",
        "204 No Content. 응답 본문은 없습니다.",
    ),
    ("get", "/api/v1/tags"): _guide(
        "관심사 태그 카탈로그 조회",
        "인증 없이 호출할 수 있는 TAG-01 전체 목록입니다. 화면에는 `category`별로 묶어 `label`을 보여주고, "
        "저장 요청에는 사람이 읽는 label이 아니라 안정적인 `code`를 사용하세요.",
        "200과 43개 태그를 반환합니다.",
    ),
    ("get", "/api/v1/users/me"): _guide(
        "내 프로필 조회",
        "로그인 사용자의 프로필, UI 모드, 미성년 여부, 비친구 요청 설정, 모드별 상세 설정과 관심사 태그를 "
        "한 번에 반환합니다. 앱 초기화 후 전역 사용자 상태의 기준으로 사용하세요.",
        "200과 본인 전용 프로필을 반환합니다.",
    ),
    ("patch", "/api/v1/users/me"): _guide(
        "내 프로필 수정",
        "보낸 필드만 변경합니다. `bio`는 최대 300자이며 전화번호·이메일·외부 메신저 ID가 감지되면 거부됩니다. "
        "성공 응답 전체를 기존 사용자 상태에 병합하는 대신 교체하면 서버 정본과 쉽게 동기화됩니다.",
        "200과 변경 후 전체 내 프로필을 반환합니다.",
        request={"nickname": "새닉네임", "bio": "영화와 산책을 좋아해요.", "profile_image_url": "/uploads/profile.jpg"},
        errors={400: "자기소개 연락처 포함 또는 닉네임 정책 위반.", 409: "이미 사용 중인 닉네임입니다."},
    ),
    ("put", "/api/v1/users/me/tags"): _guide(
        "관심사 태그 전체 교체",
        "부분 추가가 아니라 전체 교체입니다. 현재 선택한 태그 코드 전부를 보내며 최대 10개입니다. "
        "빈 배열은 모든 관심사 태그를 해제합니다.",
        "200과 변경 후 전체 내 프로필을 반환합니다.",
        request={"tag_codes": ["walking", "movie", "small_talk"]},
        errors={400: "중복 제거 후 태그가 10개를 초과합니다.", 404: "카탈로그에 없는 태그 코드가 포함되었습니다."},
    ),
    ("patch", "/api/v1/users/me/settings"): _guide(
        "내 설정 수정",
        "보낸 설정만 변경합니다. `mode_settings`는 선택한 접근성 UI의 세부 설정을 저장하는 JSON 객체입니다. "
        "미성년자의 초기 비친구 요청 차단도 사용자가 여기서 변경할 수 있습니다.",
        "200과 변경 후 전체 내 프로필을 반환합니다.",
        request={"stranger_requests_allowed": False, "mode_settings": {"font_scale": 1.2, "simple_labels": True}},
    ),
    ("put", "/api/v1/users/me/mode"): _guide(
        "UI 모드 변경",
        "`visual`, `hearing`, `developmental`, `default` 중 하나로 변경합니다. 같은 값을 다시 보내도 성공하며, "
        "실제 변경은 서버 이력에 기록됩니다. 응답을 받은 뒤 화면 테마를 적용하세요.",
        "200과 변경 후 전체 내 프로필을 반환합니다.",
        request={"ui_mode": "developmental"},
    ),
    ("delete", "/api/v1/users/me"): _guide(
        "회원 탈퇴",
        "`posts_action=anonymize`는 게시물·댓글을 '탈퇴한 사용자'로 남기고, `delete`는 함께 삭제합니다. "
        "복구할 수 없는 작업이므로 프론트에서 명시적 확인 후 호출하고 성공 시 모든 토큰을 폐기하세요.",
        "204 No Content. 같은 소셜 계정은 30일 동안 재가입할 수 없습니다.",
        request={"posts_action": "anonymize"},
    ),
    ("get", "/api/v1/users/{user_id}"): _guide(
        "다른 사용자 프로필 조회",
        "공개 가능한 닉네임·자기소개·이미지·관심사만 반환합니다. 생년월일, 미성년 여부, UI 모드는 노출하지 "
        "않습니다. 존재하지 않거나 어느 방향이든 차단 관계면 같은 404를 사용합니다.",
        "200과 공개 프로필을 반환합니다.",
        errors={404: "사용자가 없거나 차단 관계입니다. 두 경우를 화면에서 구분하지 마세요."},
    ),
    ("post", "/api/v1/posts"): _guide(
        "텍스트·사진 게시물 작성",
        "제목, 단일 카테고리, 본문을 보내고 필요하면 `/media/images`에서 받은 최대 3개의 `media_id`를 연결합니다. "
        "카테고리는 `daily`, `info`, `hobby`, `concern`, `meetup` 중 하나이며 성공 즉시 공개됩니다. "
        "영상은 이 API가 아니라 `/media/videos`로 드래프트를 만든 뒤 publish 흐름을 사용하세요.",
        "201과 공개된 게시물 전체를 반환합니다.",
        request={"title": "오늘의 공원 산책", "category": "daily", "content": "오늘 공원에서 산책했어요.", "media_ids": [UUID_A]},
        errors={400: "영상 media_id 사용 또는 사진 3장 초과.", 403: "다른 사용자의 미디어이거나 이미 사용된 미디어.", 404: "없는 media_id 포함."},
    ),
    ("get", "/api/v1/feed"): _guide(
        "홈 피드 조회",
        "최신 공개 게시물을 커서 기반으로 조회합니다. 차단 관계 게시물은 양방향으로 제외됩니다. "
        "`category`로 한 종류만 필터링하고 `q`로 제목과 본문을 부분 검색할 수 있습니다. 두 값을 생략하면 전체입니다. "
        "다음 페이지는 응답의 `next_cursor`를 그대로 전달하고, null이면 더 불러오지 마세요. `limit`은 1~50입니다.",
        "200과 `items`, `next_cursor`를 반환합니다.",
        errors={400: "cursor가 서버에서 발급한 형식이 아닙니다."},
    ),
    ("get", "/api/v1/posts/{post_id}"): _guide(
        "게시물 상세 조회",
        "공개 게시물 또는 작성자 본인의 영상 드래프트를 조회합니다. 미디어의 AI 설명·자막 상태도 함께 반환됩니다. "
        "차단 관계와 접근할 수 없는 드래프트는 404로 통일됩니다.",
        "200과 게시물 상세를 반환합니다.",
        errors={404: "게시물이 없거나 현재 사용자에게 보이지 않습니다."},
    ),
    ("patch", "/api/v1/posts/{post_id}"): _guide(
        "게시물 내용 수정",
        "작성자만 제목·카테고리·본문을 수정할 수 있으며 변경할 필드만 보냅니다. 미디어 구성은 이 API에서 바꾸지 않습니다. "
        "성공 응답으로 상세 화면과 피드 캐시의 해당 게시물을 갱신하세요.",
        "200과 수정된 게시물 전체를 반환합니다.",
        request={"title": "수정한 제목", "category": "info", "content": "수정한 게시물 내용입니다."},
        errors={403: "작성자가 아닙니다.", 404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("delete", "/api/v1/posts/{post_id}"): _guide(
        "게시물 삭제",
        "작성자만 삭제할 수 있습니다. 성공 후 목록·상세 캐시에서 게시물과 연결 댓글·좋아요를 제거하세요.",
        "204 No Content. 응답 본문은 없습니다.",
        errors={403: "작성자가 아닙니다.", 404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("get", "/api/v1/posts/{post_id}/caption-status"): _guide(
        "영상 자막 상태 조회",
        "영상 드래프트 작성자만 폴링합니다. `processing` 동안 간격을 두고 재조회하고, `done`이면 publish 가능, "
        "`failed`이면 사용자에게 재시도 또는 자막 없이 게시 선택을 보여주세요.",
        "200과 `caption_status`를 반환합니다.",
        errors={404: "본인 게시물이 아니거나 영상이 없습니다."},
    ),
    ("post", "/api/v1/posts/{post_id}/caption/retry"): _guide(
        "실패한 영상 자막 재시도",
        "작성자 본인의 비공개 영상 드래프트에서 `caption_status=failed`일 때만 호출합니다. 성공하면 상태를 "
        "`processing`으로 바꾸고 사용자·서비스 전체 일일 한도를 새로 예약합니다. 202를 받은 뒤 기존 "
        "caption-status API를 다시 폴링하고, 중복 클릭으로 병렬 호출하지 마세요.",
        "202와 `caption_status=processing`을 반환하며 자막 작업을 다시 시작합니다.",
        errors={
            404: "본인 드래프트가 아니거나 영상이 없습니다.",
            409: "실패 상태가 아니거나 이미 공개됐거나 원본 파일이 없습니다.",
            429: "게시물·채팅 합산 사용자 일일 영상 한도 초과.",
            503: "서비스 전체 일일 STT 예산 상한 초과. detail.code를 표시하고 다음 날 재시도합니다.",
        },
    ),
    ("post", "/api/v1/posts/{post_id}/publish"): _guide(
        "영상 드래프트 게시",
        "제목·단일 카테고리·본문을 최종 요청에 포함해 자막 생성이 끝난 영상 드래프트를 공개합니다. "
        "`processing`이면 게시 버튼을 잠시 비활성화하세요. "
        "자막 실패 시에만 사용자 확인 후 `allow_no_caption=true`로 다시 호출할 수 있습니다.",
        "200과 공개된 게시물 전체를 반환합니다.",
        request={"title": "공원 산책 영상", "category": "daily", "content": "오늘 산책 영상입니다.", "allow_no_caption": False},
        errors={400: "이미 공개되었거나 자막 실패 후 명시적 동의가 없습니다.", 404: "본인 드래프트가 아닙니다.", 409: "자막 생성 중입니다."},
    ),
    ("post", "/api/v1/posts/{post_id}/like"): _guide(
        "게시물 좋아요",
        "멱등 처리됩니다. 이미 좋아요한 게시물에 다시 호출해도 오류 없이 현재 상태와 개수를 반환합니다.",
        "200과 `liked=true`, 최신 `like_count`를 반환합니다.",
        errors={404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("delete", "/api/v1/posts/{post_id}/like"): _guide(
        "게시물 좋아요 취소",
        "멱등 처리됩니다. 좋아요하지 않은 게시물이어도 현재 상태를 반환하므로 낙관적 UI를 서버 값으로 보정하세요.",
        "200과 `liked=false`, 최신 `like_count`를 반환합니다.",
        errors={404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("get", "/api/v1/posts/{post_id}/comments"): _guide(
        "댓글 목록 조회",
        "게시물의 댓글을 시간순으로 반환합니다. 탈퇴한 작성자는 id 없이 '탈퇴한 사용자'로 직렬화됩니다.",
        "200과 댓글 `items`를 반환합니다.",
        errors={404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("post", "/api/v1/posts/{post_id}/comments"): _guide(
        "댓글 작성",
        "사용자가 최종 확인한 텍스트를 게시합니다. AI 댓글 추천 결과는 자동 게시되지 않으므로 선택한 문장을 이 API에 "
        "명시적으로 전달해야 합니다.",
        "201과 작성된 댓글을 반환합니다.",
        request={"content": "산책하기 좋은 날씨네요!"},
        errors={404: "게시물이 없거나 차단 관계입니다."},
    ),
    ("patch", "/api/v1/comments/{comment_id}"): _guide(
        "댓글 수정",
        "댓글 작성자만 내용을 수정할 수 있습니다. 성공 응답의 `updated_at`과 내용을 댓글 목록에 반영하세요.",
        "200과 수정된 댓글을 반환합니다.",
        request={"content": "수정한 댓글입니다."},
        errors={403: "댓글 작성자가 아닙니다.", 404: "댓글이 없습니다."},
    ),
    ("delete", "/api/v1/comments/{comment_id}"): _guide(
        "댓글 삭제",
        "댓글 작성자만 삭제할 수 있습니다. 성공 후 화면 목록과 게시물의 댓글 개수를 함께 갱신하세요.",
        "204 No Content. 응답 본문은 없습니다.",
        errors={403: "댓글 작성자가 아닙니다.", 404: "댓글이 없습니다."},
    ),
    ("post", "/api/v1/media/images"): _guide(
        "게시물 사진 업로드",
        "`multipart/form-data`의 동일한 `files` 필드로 최대 3장을 전송합니다. 반환된 `media_id`는 아직 게시물에 "
        "연결되지 않았으므로 `/posts` 작성 요청의 `media_ids`에 넣어야 공개됩니다.",
        "201과 업로드된 미디어 ID·URL 목록을 반환합니다.",
        errors={400: "3장 초과 또는 지원하지 않는 이미지 MIME 형식.", 413: "이미지 한 장의 크기 제한 초과."},
    ),
    ("post", "/api/v1/media/videos"): _guide(
        "게시물 영상 업로드·자막 시작",
        "`file`과 프론트가 측정한 1 이상 `duration_seconds`를 multipart로 보냅니다. 서버가 MIME·실제 컨테이너·"
        "비디오 트랙·길이를 다시 검증하며 MP4·WebM·QuickTime을 지원합니다. STT에는 원본 영상 대신 "
        "25MB 이하 M4A 음성을 보냅니다. 성공 즉시 `processing` 드래프트가 생성되고, "
        "`post_id`로 자막 상태를 폴링한 뒤 별도 publish를 호출해야 공개됩니다.",
        "201과 드래프트 `post_id`, `media_id`, 초기 자막 상태를 반환합니다.",
        errors={
            400: "길이 값 오류, 실제 3분 초과, MIME·콘테이너 불일치, 비디오 트랙 없음 또는 손상된 영상.",
            413: "200MB 초과.",
            429: "게시물·채팅 합산 사용자 일일 영상 한도 초과.",
            503: "서비스 전체 일일 STT 예산 상한 초과. detail.code=STT_DAILY_BUDGET_EXCEEDED.",
        },
    ),
    ("post", "/api/v1/media/transcribe"): _guide(
        "음성 입력을 텍스트로 변환",
        "음성 파일을 multipart의 `file`로 전송합니다. 반환 텍스트는 입력란 초안일 뿐 자동 게시·전송되지 않으며, "
        "사용자가 확인·수정한 뒤 해당 작성 API를 호출해야 합니다.",
        "200과 변환된 `text`를 반환합니다.",
        errors={413: "음성 파일 크기 제한 초과.", 502: "외부 음성 변환 실패."},
    ),
    ("post", "/api/v1/friends/requests"): _guide(
        "친구 요청 보내기",
        "추천 카드나 공개 프로필의 사용자 UUID를 `receiver_id`로 보냅니다. 자기 자신, 이미 친구, 처리 중 요청은 "
        "거부되며 차단 관계는 존재 여부를 숨기기 위해 404입니다.",
        "201과 pending 친구 요청을 반환합니다.",
        request={"receiver_id": UUID_B},
        errors={400: "자기 자신, 이미 친구 또는 처리 중인 요청.", 404: "사용자가 없거나 차단 관계입니다."},
    ),
    ("get", "/api/v1/friends/requests"): _guide(
        "친구 요청함 조회",
        "`box=received`는 받은 요청, `box=sent`는 보낸 요청입니다. 기본값은 received이며 pending 요청만 표시됩니다.",
        "200과 친구 요청 `items`를 반환합니다.",
    ),
    ("post", "/api/v1/friends/requests/{request_id}/accept"): _guide(
        "친구 요청 수락",
        "받은 pending 요청의 수신자만 호출할 수 있습니다. 성공 시 양방향 친구 관계가 생성되고 요청자에게 알림이 갑니다.",
        "200과 accepted 상태의 요청을 반환합니다.",
        errors={403: "현재 사용자가 요청 수신자가 아닙니다.", 404: "없거나 이미 처리된 요청입니다."},
    ),
    ("post", "/api/v1/friends/requests/{request_id}/decline"): _guide(
        "친구 요청 거절",
        "받은 pending 요청의 수신자만 호출할 수 있습니다. 거절한 두 사용자는 30일 동안 서로의 친구 추천에서 제외됩니다.",
        "200과 declined 상태의 요청을 반환합니다.",
        errors={403: "현재 사용자가 요청 수신자가 아닙니다.", 404: "없거나 이미 처리된 요청입니다."},
    ),
    ("post", "/api/v1/friends/requests/{request_id}/cancel"): _guide(
        "보낸 친구 요청 취소",
        "pending 요청을 보낸 사용자만 호출할 수 있습니다. 받은 요청의 거절과 달리 추천 30일 제외 사유로 사용되지 않습니다.",
        "200과 cancelled 상태의 요청을 반환합니다.",
        errors={403: "현재 사용자가 요청자가 아닙니다.", 404: "없거나 이미 처리된 요청입니다."},
    ),
    ("get", "/api/v1/friends"): _guide(
        "친구 목록 조회",
        "현재 사용자의 양방향 친구 목록입니다. 채팅방 생성과 친구 전용 미디어 전송 UI의 기준으로 사용하세요.",
        "200과 공개 프로필 요약 `items`를 반환합니다.",
    ),
    ("delete", "/api/v1/friends/{user_id}"): _guide(
        "친구 삭제",
        "친구 관계를 해제합니다. 이미 관계가 없어도 성공하므로 화면과 채팅 미디어 전송 가능 상태를 즉시 갱신하세요.",
        "204 No Content. 응답 본문은 없습니다.",
    ),
    ("get", "/api/v1/blocks"): _guide(
        "차단 목록 조회",
        "내가 차단한 사용자만 반환합니다. 상대가 나를 차단한 사실은 개인정보 보호를 위해 목록에 나타나지 않습니다.",
        "200과 차단 사용자 요약 `items`를 반환합니다.",
    ),
    ("post", "/api/v1/blocks"): _guide(
        "사용자 차단",
        "차단하면 친구 관계가 해제되고 게시물·프로필·친구 요청·채팅·추천 접점이 양방향으로 제거됩니다. "
        "같은 사용자를 다시 차단해도 성공하는 멱등 동작입니다.",
        "201과 `{\"blocked\": true}`를 반환합니다.",
        request={"user_id": UUID_B},
        errors={400: "자기 자신을 차단하려는 요청.", 404: "사용자가 없습니다."},
    ),
    ("delete", "/api/v1/blocks/{user_id}"): _guide(
        "사용자 차단 해제",
        "내가 설정한 차단을 해제합니다. 친구 관계와 이전 채팅 관계는 자동 복구되지 않습니다.",
        "204 No Content. 응답 본문은 없습니다.",
    ),
    ("get", "/api/v1/chat/rooms"): _guide(
        "활성 채팅방 목록 조회",
        "수락된 active 채팅방을 반환합니다. 각 방의 `unread_count`, 전역 `unread_total`, 상대 발신 제한 상태를 "
        "서버 값으로 표시하세요.",
        "200과 채팅방 목록 및 전체 미읽음 수를 반환합니다.",
    ),
    ("post", "/api/v1/chat/rooms"): _guide(
        "채팅방 생성 또는 조회",
        "상대 사용자와 기존 채팅방이 있으면 재사용합니다. 친구면 active, 비친구면 request 상태로 만들어집니다. "
        "미성년 보호 설정이나 차단으로 불가능한 경우 상대 존재를 숨겨 404를 반환합니다.",
        "200과 생성되거나 기존에 존재한 채팅방을 반환합니다.",
        request={"user_id": UUID_B},
        errors={400: "자기 자신과의 채팅 요청.", 404: "사용자가 없거나 정책상 채팅할 수 없습니다."},
    ),
    ("get", "/api/v1/chat/requests"): _guide(
        "메시지 요청함 조회",
        "내가 수신한 request 상태의 비친구 채팅방만 반환합니다. 수락 전에는 미디어를 보낼 수 없습니다.",
        "200과 요청 채팅방 목록을 반환합니다.",
    ),
    ("post", "/api/v1/chat/rooms/{room_id}/messages"): _guide(
        "텍스트 메시지 전송",
        "텍스트는 SAFE 모델 판정 후 저장·전달됩니다. 응답은 발신자 관점이라 원문은 유지되지만 판정 값은 노출하지 "
        "않습니다. 403이면 입력을 보존하고 사용자에게 전송 제한 안내를 표시하세요.",
        "201과 저장된 메시지를 반환하며 상대에게 WebSocket 이벤트를 발행합니다.",
        request={"content": "안녕하세요. 오늘 어떻게 지냈어요?"},
        errors={400: "메시지 내용 정책 위반.", 403: "차단·관계 정책 또는 SAFE 누적 전송 제한.", 404: "참여 중인 채팅방이 아닙니다."},
    ),
    ("get", "/api/v1/chat/rooms/{room_id}/messages"): _guide(
        "채팅 메시지 목록 조회",
        "최신 메시지부터 커서 페이지네이션합니다. 응답 `items`는 화면 표시 순서에 맞게 서버가 제공합니다. "
        "`next_cursor=null`이면 마지막 페이지입니다. 조회 시 읽음 커서와 상대 WebSocket 읽음 이벤트도 갱신됩니다.",
        "200과 메시지 `items`, `next_cursor`를 반환합니다.",
        errors={400: "cursor 형식이 잘못되었습니다.", 404: "참여 중인 채팅방이 아닙니다."},
    ),
    ("post", "/api/v1/chat/messages/{message_id}/reveal"): _guide(
        "주의 메시지 내용 보기",
        "수신자에게 `blurred=true`, `content=null`로 온 주의 메시지를 사용자가 명시적으로 선택했을 때만 호출합니다. "
        "자동 호출하지 말고 경고 UI를 먼저 보여주세요.",
        "200과 실제 메시지 `content`를 반환합니다.",
        errors={400: "주의 메시지가 아닙니다.", 403: "발신자이거나 해당 메시지 수신자가 아닙니다.", 404: "메시지가 없습니다."},
    ),
    ("post", "/api/v1/chat/requests/{room_id}/accept"): _guide(
        "메시지 요청 수락",
        "요청을 받은 사용자만 request 채팅방을 active로 전환합니다. 수락은 친구 관계를 자동 생성하지 않으므로 "
        "사진·영상 전송은 별도 친구 관계가 있어야 합니다.",
        "200과 active 상태의 채팅방을 반환합니다.",
        errors={400: "받은 request 상태가 아니어서 수락할 수 없습니다.", 404: "참여 중인 채팅방이 아닙니다."},
    ),
    ("post", "/api/v1/chat/restrictions/{sender_id}/release"): _guide(
        "메시지 전송 제한 해제",
        "주의 판정 누적으로 나에게 메시지를 보내지 못하게 된 상대의 제한을 수신자인 내가 해제합니다. "
        "해제 시 누적 카운터도 초기화됩니다.",
        "200과 `{\"released\": true}`를 반환합니다.",
        errors={404: "해제할 활성 제한이 없습니다."},
    ),
    ("post", "/api/v1/chat/rooms/{room_id}/media"): _guide(
        "채팅 사진·영상 전송",
        "active 상태의 친구 채팅에서만 multipart `file`을 전송합니다. 영상은 `duration_seconds`도 필요하며 자막 한도를 "
        "차감합니다. 서버가 MIME·실제 컨테이너·비디오 트랙·길이를 검증하고, STT에는 M4A 음성만 전송합니다. "
        "자막 완료·실패 시 송수신자 모두에게 `media.caption_done` "
        "또는 `media.caption_failed` 알림을 보냅니다. 미성년자–성인 간 채팅에서는 텍스트만 허용됩니다.",
        "201과 미디어 메시지를 반환하며 상대에게 WebSocket 이벤트를 발행합니다. 초기 caption_status는 processing입니다.",
        errors={
            400: "지원하지 않거나 손상된 형식, MIME·콘테이너 불일치, 비디오 트랙 없음, 길이 값 오류 또는 실제 3분 초과.",
            403: "친구·방 상태·차단·연령·전송 제한 정책 위반.",
            413: "파일 크기 제한 초과.",
            429: "사용자 일일 영상 한도 초과.",
            503: "서비스 전체 일일 STT 예산 상한 초과.",
        },
    ),
    ("get", "/api/v1/notifications"): _guide(
        "알림 목록 조회",
        "최신순으로 최대 `limit`개를 조회합니다. `read_at=null`이면 읽지 않은 알림입니다. payload 구조는 `type`에 "
        "따라 달라지므로 알 수 없는 타입도 안전하게 무시하거나 기본 알림으로 표시하세요.",
        "200과 알림 `items`를 반환합니다.",
    ),
    ("post", "/api/v1/notifications/read"): _guide(
        "알림 읽음 처리",
        "현재 사용자의 알림 UUID 목록을 한 번에 읽음 처리합니다. 다른 사용자의 ID나 이미 읽은 ID는 무시되어 "
        "재시도해도 안전합니다.",
        "200과 `{\"read\": true}`를 반환합니다.",
        request={"ids": [UUID_A, UUID_B]},
    ),
    ("get", "/api/v1/recommendations"): _guide(
        "맞춤 친구 추천 조회",
        "자신·기존 친구·양방향 차단·거절 후 30일·미성년/성인 교차 후보를 백엔드에서 제외하고 MATCH 모델로 "
        "점수화합니다. **중요:** 후보 부족과 모델 일시 장애도 HTTP 200입니다. 프론트는 요청 완료 시 항상 로딩을 "
        "끝내고, `items`가 비었으면 `message`를 표시하세요. 추천 사유에는 UI 모드·장애 정보가 포함되지 않습니다.",
        "200과 추천 `items`를 반환합니다. 결과가 없으면 `items=[]`와 사용자 안내 `message`가 함께 옵니다.",
        examples={
            "success": {"summary": "추천 성공", "value": {"items": [{"user_id": UUID_B, "nickname": "산책친구", "bio": "영화와 산책을 좋아해요.", "profile_image_url": None, "tags": ["walking", "movie"], "score": 0.87, "reasons": ["관심사가 비슷해요", "비슷한 연령대예요"]}], "message": None}},
            "insufficient": {"summary": "추천 후보 부족", "value": {"items": [], "message": "추천 정보가 부족합니다"}},
            "temporary": {"summary": "MATCH 모델 일시 장애", "value": {"items": [], "message": "지금은 추천을 만들 수 없어요. 잠시 후 다시 시도해 주세요"}},
        },
    ),
    ("post", "/api/v1/comm/simplify"): _guide(
        "문장을 쉬운 표현으로 바꾸기",
        "사용자가 입력한 문장을 더 짧고 쉬운 평문으로 변환합니다. 응답은 Markdown 코드블록이나 JSON 문자열이 아닌 "
        "일반 텍스트입니다. `original`과 `result` 전환 UI를 제공하고 자동 저장·전송하지 마세요.",
        "200과 변환 결과 `result`, 입력 원문 `original`을 반환합니다.",
        request={"text": "금일 약속 장소로 정시에 도착할 예정입니다."},
        errors={503: "AI 소통 코치를 일시적으로 사용할 수 없습니다."},
    ),
    ("post", "/api/v1/comm/complete"): _guide(
        "작성 중인 문장 완성 후보",
        "최대 2000자의 작성 중 텍스트를 보내면 일반 텍스트 후보 목록을 반환합니다. 후보를 눌러 입력란에 넣을 수 "
        "있지만 사용자 확인 없이 게시하거나 전송하면 안 됩니다.",
        "200과 `suggestions: string[]`를 반환합니다.",
        request={"text": "오늘 만나서 정말"},
        errors={503: "AI 소통 코치를 일시적으로 사용할 수 없습니다."},
    ),
    ("post", "/api/v1/comm/comments"): _guide(
        "게시물 댓글 후보 추천",
        "공개되고 차단 관계가 아닌 게시물 UUID를 보냅니다. 서버가 게시물 본문과 최근 댓글을 조회해 평문 댓글 후보만 "
        "반환합니다. 선택 후 실제 등록은 `/posts/{post_id}/comments`를 별도로 호출해야 합니다.",
        "200과 `suggestions: string[]`를 반환합니다.",
        request={"post_id": UUID_A},
        errors={404: "게시물이 없거나 비공개·차단 관계입니다.", 503: "AI 소통 코치를 일시적으로 사용할 수 없습니다."},
    ),
    ("post", "/api/v1/comm/replies"): _guide(
        "채팅 답장 후보 추천",
        "참여 중인 채팅방 UUID를 보냅니다. 서버는 최근 10개 공개 가능 텍스트만 사용하며, 미열람 주의 메시지와 분석 "
        "대기 메시지는 제외합니다. 후보 선택 후 실제 전송 API를 별도로 호출하세요.",
        "200과 `suggestions: string[]`를 반환합니다.",
        request={"room_id": UUID_A},
        errors={404: "참여 중인 채팅방이 아닙니다.", 503: "AI 소통 코치를 일시적으로 사용할 수 없습니다."},
    ),
    ("post", "/api/v1/comm/hints"): _guide(
        "대화 이어가기 힌트",
        "참여 중인 채팅방의 최근 공개 가능 텍스트를 바탕으로 대화 방향 힌트를 제공합니다. 힌트는 메시지 본문이 "
        "아니므로 바로 전송하지 말고 별도 도움말 영역에 표시하세요.",
        "200과 `hints: string[]`를 반환합니다.",
        request={"room_id": UUID_A},
        errors={404: "참여 중인 채팅방이 아닙니다.", 503: "AI 소통 코치를 일시적으로 사용할 수 없습니다."},
    ),
}


ERROR_SCHEMA = {
    "type": "object",
    "required": ["detail"],
    "properties": {
        "detail": {
            "type": "string",
            "description": "사용자에게 표시하거나 상황별 UI로 변환할 수 있는 한국어 오류 메시지",
            "example": "요청을 처리할 수 없습니다",
        }
    },
}


PARAMETER_DESCRIPTIONS = {
    "provider": "소셜 로그인 제공자: `kakao`, `google`, 개발 환경에서는 `mock`.",
    "code": "OAuth 제공자가 발급한 일회용 authorization code. 프론트가 임의 생성하지 않습니다.",
    "error": "사용자가 동의를 거부했거나 OAuth 제공자가 전달한 오류 코드.",
    "refresh_token": "httpOnly 쿠키. JavaScript에서 읽지 말고 credentials 포함 요청으로 자동 전송합니다.",
    "user_id": "대상 사용자의 UUID.",
    "post_id": "대상 게시물 또는 영상 드래프트의 UUID.",
    "comment_id": "대상 댓글의 UUID.",
    "request_id": "친구 요청의 UUID.",
    "room_id": "현재 사용자가 참여 중인 채팅방 UUID.",
    "message_id": "채팅 메시지 UUID.",
    "sender_id": "내가 해제할 전송 제한의 상대 발신자 UUID.",
    "cursor": "이전 응답의 `next_cursor`를 수정 없이 전달합니다. 첫 페이지에서는 생략합니다.",
    "limit": "한 번에 받을 항목 수. 엔드포인트별 최소·최대값은 입력란 제약을 따릅니다.",
    "category": "게시물 단일 카테고리 코드: `daily`, `info`, `hobby`, `concern`, `meetup`.",
    "q": "제목과 본문에서 찾을 부분 검색어. 앞뒤 공백은 무시하며 최대 100자입니다.",
    "box": "친구 요청함 방향: `received`(받음, 기본값) 또는 `sent`(보냄).",
}


def _add_error_response(operation: dict[str, Any], status: int, description: str) -> None:
    operation.setdefault("responses", {})[str(status)] = {
        "description": description,
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {"detail": description.split(".", 1)[0]},
            }
        },
    }


def install_openapi(app: FastAPI) -> None:
    """상세한 문서 스키마를 앱에 설치한다."""

    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
            contact=app.contact,
        )
        schema.setdefault("components", {}).setdefault("schemas", {})[
            "ErrorResponse"
        ] = ERROR_SCHEMA
        schema["components"].setdefault("securitySchemes", {})["RefreshCookie"] = {
            "type": "apiKey",
            "in": "cookie",
            "name": "refresh_token",
            "description": (
                "로그인·회원가입 시 설정되는 httpOnly 쿠키입니다. JavaScript로 읽지 말고 "
                "브라우저 요청에 credentials를 포함해 자동 전송합니다."
            ),
        }

        for (method, path), guide in OPERATION_GUIDES.items():
            operation = schema["paths"][path][method]
            operation["summary"] = guide.summary
            operation["description"] = (
                f"{guide.description}\n\n**성공 응답**\n\n{guide.success}\n\n"
                "**프론트 공통 처리**\n\n인증이 필요한 작업은 `Authorization: Bearer <access_token>`을 "
                "전송하고, 완료·실패 모두에서 로딩 상태를 해제하세요."
            )
            for parameter in operation.get("parameters", []):
                if parameter["name"] in PARAMETER_DESCRIPTIONS:
                    parameter["description"] = PARAMETER_DESCRIPTIONS[parameter["name"]]
                if parameter["name"].endswith("_id") or parameter["name"] == "user_id":
                    parameter["example"] = UUID_A

            for response_key in guide.remove_responses:
                operation.get("responses", {}).pop(response_key, None)
            success_status = guide.success_status or next(
                (status for status in operation.get("responses", {}) if status.startswith("2")),
                "200",
            )
            success_response = operation.setdefault("responses", {}).setdefault(
                success_status, {"description": guide.success}
            )
            success_response["description"] = guide.success
            if guide.response_examples:
                media = success_response.setdefault("content", {}).setdefault(
                    "application/json", {}
                )
                media["examples"] = guide.response_examples

            if guide.request_example is not None:
                content = operation.get("requestBody", {}).get("content", {})
                json_media = content.get("application/json")
                if json_media is not None:
                    json_media["example"] = guide.request_example

            # FastAPI가 자동 생성하는 422 설명을 실제 의미로 교체한다.
            validation = operation.get("responses", {}).get("422")
            if validation is not None:
                validation["description"] = "경로·쿼리·본문 형식 또는 필드 제약 조건이 올바르지 않습니다."

            if operation.get("security"):
                _add_error_response(operation, 401, "Access token이 없거나 만료·위조되었습니다.")
            for status, error_description in guide.errors.items():
                _add_error_response(operation, status, error_description)

        # 브라우저가 현재 문서 호스트를 그대로 API 기준 주소로 사용한다.
        schema["servers"] = [
            {"url": "/", "description": "현재 서버"},
            {"url": "http://localhost:8000", "description": "로컬 개발 서버"},
        ]
        schema["paths"]["/api/v1/auth/refresh"]["post"]["security"] = [
            {"RefreshCookie": []}
        ]
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
