# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 131 files · ~66,247 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1311 nodes · 3352 edges · 139 communities (93 shown, 46 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 293 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dab0391c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- users.py
- stt.py
- User
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- blocks.py
- register
- v1/chat.py
- auth_header
- quota.py
- test_comm.py
- v1/comm.py
- SafetyUnavailable
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_match.py
- _BorrowedSession
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- test_auth.py
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- Base
- 11. AI 안심 채팅
- 1. 서비스 개요
- v1/auth.py
- 4. 사용자 정책
- 10. 1:1 채팅
- 12. 시각장애인 모드
- test_openapi.py
- SAFE 이진 v6 배포 검증
- 17. 외부 AI 사용 및 데이터 처리 원칙
- 6. 회원가입 및 계정
- 0. 문서 정보
- services/chat.py
- SAFE 최신 호환 서빙 재평가
- 13. 청각장애인 모드
- 18. 기술 구성
- 19. 비기능 요구사항
- 5. 공통 화면 구조
- 9. 친구·차단
- MATCH v2 배포 성능 평가
- friendships 테이블(정규화 쌍)
- WebSocket + Redis pub/sub 팬아웃
- withdrawn_socials 테이블
- test_chat.py
- _Redis
- SAFE 그루밍 평가 결과
- send_media
- call_signaling.py
- Funnel 고정 URL
- Tailscale Funnel 임시 배포 가이드
- CORS 오리진 명시 설정
- Cloudflare Tunnel 임시 배포 가이드
- OpenAI 비용 노출 위험 (vision/stt)
- refresh 쿠키 SameSite=None; Secure (크로스오리진)
- 예시 태스크: 게시글 수정 API (PUT /posts/{id})
- Ralph 루프 태스크 가이드
- --max-iterations 필수 안전장치
- pytest 그린 = 완료 판정 기준
- forbidden_nicknames 테이블
- notifications 테이블
- social_identities 테이블
- user_interest_tags 테이블
- user_mode_history 테이블
- tools/__init__.py
- test_schema.py
- Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록
- Q: 영상 자막 부분 기능 감사해줘
- thisabled-backend
- Q: ㅇㅋ 결함들 해결 방안 추천해줘
- Q: 영상 자막 결함 해결 방안 구현
- v1/media.py
- notifications.py
- 스키마 v3 baseline(빅뱅)
- 만나이·연령대 유틸(age.py)
- APScheduler 인프로세스 크론(24h 청소·재분석)
- blocks 테이블
- chat_messages 테이블(safety_status)
- chat_rooms 테이블(request|active)
- comments 테이블
- friend_requests 테이블
- interest_tags 테이블
- match-model HTTP 경계(SBERT+LightGBM, mock)
- OAuth mock 제공자(env 토글, 실키 교체)
- post_likes 테이블
- post_media 테이블
- posts 테이블
- safety-model HTTP 경계(자체 안전 모델, mock)
- send_restrictions 테이블(SAFE-05)
- signup_token(단기 가입 토큰, 30분)
- conftest.py
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- match_model.py
- scheduler.py
- vision.py
- test_notifications.py
- env.py
- main.py
- Chat Read Status Implementation Plan
- test_friends.py
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- upload_video
- generate_caption
- CHAT-05 음성·영상 통화 시그널링 설계
- media_probe.py
- safety_model.py
- RestrictionReleaseOut
- list_messages
- fake_ai
- test_calls.py

## God Nodes (most connected - your core abstractions)
1. `register()` - 88 edges
2. `User` - 86 edges
3. `auth_header()` - 85 edges
4. `StrictRequest` - 73 edges
5. `_Redis` - 56 edges
6. `_post()` - 36 edges
7. `ChatMessage` - 31 edges
8. `Base` - 29 edges
9. `send_media()` - 26 edges
10. `UiMode` - 26 edges

## Surprising Connections (you probably didn't know these)
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `Post`  [INFERRED]
  tests/test_withdrawal.py → app/models/post.py
- `test_withdraw_delete_removes_posts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_withdrawal.py → app/models/post.py
- `test_photo_post_gets_description_on_publish()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py

## Import Cycles
- None detected.

## Communities (139 total, 46 thin omitted)

### Community 0 - "users.py"
Cohesion: 0.06
Nodes (76): AsyncSession, BaseModel, get, RecommendationListOut, RecommendationOut, recommendations(), me(), _me_out() (+68 more)

### Community 1 - "stt.py"
Cohesion: 0.23
Nodes (11): _extract_audio_to_m4a(), _get_client(), AsyncOpenAI, Path, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막). 엔드포인트는 `stt.transcribe(...)` 를…, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 최대 200MB 영상을 STT 상한 안의 단일 채널 M4A 음성으로 정규화한다., 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01). (+3 more)

### Community 2 - "User"
Cohesion: 0.08
Nodes (80): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), _contains_pattern(), create_comment(), create_post(), _cursor_position() (+72 more)

### Community 3 - "ai_media.py"
Cohesion: 0.15
Nodes (25): content_type_from_path(), STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다., PostMedia, 게시물 미디어 (사진≤3·영상 1개는 앱 검증). VISION 설명·CAPTION 자막 부착., _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job() (+17 more)

### Community 5 - "friends.py"
Cohesion: 0.10
Nodes (43): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+35 more)

### Community 6 - "blocks.py"
Cohesion: 0.24
Nodes (13): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, delete, get, UUID (+5 more)

### Community 7 - "register"
Cohesion: 0.19
Nodes (20): RuntimeError, mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소., 새 Starlette에서는 응답 본문 뒤 background task가 별도 스케줄될 수 있어 완료를 기다린다., test_caption_failure_requires_explicit_choice_and_refunds(), test_cleanup_deletes_stale_drafts(), test_failed_caption_can_be_retried() (+12 more)

### Community 8 - "v1/chat.py"
Cohesion: 0.25
Nodes (21): _author(), _message_preview(), CHAT-01~05 — 1:1 채팅 · 요청함 · 읽음 · WebRTC 시그널링., _room_out(), CallKind, CallSignalType, CallCreateIn, CallOut (+13 more)

### Community 9 - "auth_header"
Cohesion: 0.17
Nodes (23): auth_header(), _post(), FEED-01 피드 · POST-01~03 게시물·댓글·좋아요., test_blocked_users_posts_hidden_both_ways(), test_comment_crud_and_count(), test_edit_delete_requires_author(), test_feed_cursor_pagination(), test_feed_filters_category_and_searches_title_or_content() (+15 more)

### Community 10 - "quota.py"
Cohesion: 0.12
Nodes (32): consume_vision(), 일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백., caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute() (+24 more)

### Community 11 - "test_comm.py"
Cohesion: 0.29
Nodes (6): COMM-01~05 — 쉬운 문장·문장 완성·댓글·답장 추천·대화 힌트., test_post_comments_hide_blocked_post(), test_post_comments_use_post_and_latest_10_comments(), test_simplify_and_complete(), fixture, safety()

### Community 12 - "v1/comm.py"
Cohesion: 0.14
Nodes (33): _coach(), complete(), hints(), HintsOut, _post_context(), PostIn, AsyncSession, BaseModel (+25 more)

### Community 13 - "SafetyUnavailable"
Cohesion: 0.22
Nodes (7): get_safety_client(), Exception, SAFE-01 — 자체 안전 모델 HTTP 클라이언트 (별도 모델 서버 경계, AI 팀 담당). 텍스트 위험 판정에는 외부 AI를 사용하지…, 모델 서버 장애·지연 — 친구 텍스트는 unanalyzed 전달, 비친구는 pending 보류., → 'safe' | 'flagged'. 미성년 수신자는 민감(낮은) 임계값 (§4.5)., FastAPI 의존성 — 테스트에서 fake로 override., SafetyUnavailable

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics(), load_cases() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.2)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~05 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 18 - "test_match.py"
Cohesion: 0.18
Nodes (9): FakeMatch, match(), fixture, MATCH — 후보 제외 규칙은 백엔드 강제, 점수·사유는 모델 서버 (mock/fake)., 도메인 default는 MATCH 서버가 허용하는 중립값으로 직렬화한다., test_default_mode_uses_neutral_model_value(), test_empty_pool_message(), test_exclusion_rules_enforced_by_backend() (+1 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "test_auth.py"
Cohesion: 0.10
Nodes (31): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), test_refresh_rotates_access_token() (+23 more)

### Community 23 - "services/comm.py"
Cohesion: 0.07
Nodes (24): _collect_strings(), CommUnavailable, get_comm_client(), OpenAICommClient, _plain_text(), COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상). 버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개…, FastAPI 의존성 — 테스트에서 fake로 override., 외부 코칭 결과를 안전한 API 응답으로 만들 수 없을 때. (+16 more)

### Community 24 - "Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함, Source Nodes

### Community 25 - "Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘

### Community 26 - "Global Constraints"
Cohesion: 0.29
Nodes (6): Global Constraints, SAFE Grooming Evaluation Implementation Plan, Task 1: Add the evaluation fixture and pure metric tests, Task 2: Implement the pure evaluator and CLI, Task 3: Run the real SAFE evaluation, Task 4: Verify and document limitations

### Community 27 - "SAFE 그루밍 평가 설계"
Cohesion: 0.29
Nodes (6): SAFE 그루밍 평가 설계, 목적, 범위, 비범위, 성공 기준, 실행 흐름

### Community 28 - "14. 발달장애인 모드 및 AI 소통 코치"
Cohesion: 0.29
Nodes (7): 14. 발달장애인 모드 및 AI 소통 코치, COMM-01 쉬운 문장 변환, COMM-02 문장 완성, COMM-03 댓글·답장 추천, COMM-04 대화 힌트, COMM-05 데이터 처리 원칙, DEV-01 기본 UI

### Community 29 - "7. 피드·게시물·댓글"
Cohesion: 0.29
Nodes (7): 7. 피드·게시물·댓글, CAPTION-01 영상 자동 자막, FEED-01 홈 피드, POST-01 게시물 작성, POST-02 수정·삭제, POST-03 좋아요·댓글, VISION-01 AI 사진 설명

### Community 30 - "Base"
Cohesion: 0.17
Nodes (14): Base, AiResultCache, Notification, 알림 (§16). WS 푸시와 병행 저장., 동일 미디어 해시 캐싱 (VISION-01·CAPTION-01 중복 호출 방지, 비용 방어)., ForbiddenNickname, 운영자 관리 금칙어 사전 (ACC-01 닉네임 정책)., 모드 변경 이력 (§5.2, 베타테스트 분석용). (+6 more)

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 33 - "v1/auth.py"
Cohesion: 0.05
Nodes (49): authorize(), callback(), _frontend_redirect(), logout(), _oauth_state_key(), AsyncSession, get, UUID (+41 more)

### Community 34 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 35 - "10. 1:1 채팅"
Cohesion: 0.33
Nodes (6): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설), CHAT-05 음성·영상 통화

### Community 36 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 37 - "test_openapi.py"
Cohesion: 0.16
Nodes (19): _add_error_response(), _guide(), install_openapi(), OperationGuide, Any, FastAPI, 프론트엔드 구현자를 위한 OpenAPI 문서 보강. FastAPI의 기본 스키마는 타입은 정확하지만 비즈니스 상태와 화면 처리 방법을 설명하지…, 프론트엔드 계약 문서가 라우트 변경 뒤에도 빠지거나 퇴행하지 않도록 검증. (+11 more)

### Community 38 - "SAFE 이진 v6 배포 검증"
Cohesion: 0.33
Nodes (5): FN, FP, SAFE 이진 v6 배포 검증, 백엔드 회귀 확인, 판정

### Community 39 - "17. 외부 AI 사용 및 데이터 처리 원칙"
Cohesion: 0.40
Nodes (5): 17.1 자체 처리 (외부 미전송), 17.2 외부 AI API 사용 (가입 시 필수 고지), 17.3 공통 처리 원칙, 17.4 관리자 기능, 17. 외부 AI 사용 및 데이터 처리 원칙

### Community 40 - "6. 회원가입 및 계정"
Cohesion: 0.40
Nodes (5): 6. 회원가입 및 계정, ACC-01 회원가입 (소셜 로그인), ACC-02 로그인·로그아웃, ACC-03 프로필, TAG-01 관심사 태그 체계 (정본)

### Community 41 - "0. 문서 정보"
Cohesion: 0.50
Nodes (4): 0.0 v2.2 주요 개정 사항, 0.1 v2.1 주요 개정 사항 (이력), 0.2 v2.0 주요 개정 사항 (이력), 0. 문서 정보

### Community 42 - "services/chat.py"
Cohesion: 0.11
Nodes (39): §CHAT-02 — request=요청함, active=일반 채팅., RoomState, ChatMessage, ChatReadState, ChatRoom, datetime, SAFE-05 관계 단위 자동 전송 제한. 누적 카운터는 별도 컬럼 없이 chat_messages에서 `flagged AND…, 1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅. 참여자는 정규화 쌍(user_a < user_b,… (+31 more)

### Community 43 - "SAFE 최신 호환 서빙 재평가"
Cohesion: 0.40
Nodes (4): SAFE 최신 호환 서빙 재평가, 결과, 결론, 실행 기준

### Community 44 - "13. 청각장애인 모드"
Cohesion: 0.50
Nodes (4): 13. 청각장애인 모드, HEAR-01 기본 UI, HEAR-02 영상 자막, HEAR-03 알림

### Community 45 - "18. 기술 구성"
Cohesion: 0.50
Nodes (4): 18.1 웹 서비스, 18.2 AI 모듈, 18.3 설계 원칙, 18. 기술 구성

### Community 46 - "19. 비기능 요구사항"
Cohesion: 0.50
Nodes (4): 19.1 접근성, 19.2 개인정보·보안, 19.3 AI 품질, 19. 비기능 요구사항

### Community 47 - "5. 공통 화면 구조"
Cohesion: 0.50
Nodes (4): 5.1 주요 화면, 5.2 UI 모드 전환, 5.3 기본 모드 (GEN-01, 신설), 5. 공통 화면 구조

### Community 48 - "9. 친구·차단"
Cohesion: 0.50
Nodes (4): 9. 친구·차단, BLOCK-01 사용자 차단, FRIEND-01 친구 요청, FRIEND-02 친구 관리

### Community 50 - "MATCH v2 배포 성능 평가"
Cohesion: 0.20
Nodes (9): 1. 기동 및 계약, 2.1 배포 번들 저장 지표, 2.2 배포 모델 독립 재평가, 2. 랭킹 품질, 3. 공정성 및 활동량 편향, 4. 실서버 지연, 5. 운영 관찰사항, 6. 최종 판정 (+1 more)

### Community 54 - "test_chat.py"
Cohesion: 0.16
Nodes (31): test_call_requires_online_active_same_age_friend(), _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), _send(), test_chat_text_is_trimmed_and_limited(), test_chat_video_gets_caption_and_notifies_both_users() (+23 more)

### Community 55 - "_Redis"
Cohesion: 0.08
Nodes (32): WS /api/v1/ws?token=<access> — 새 메시지·알림·통화 시그널 실시간 푸시. 인증은 JWT 검증만으로 처리(DB…, _relay(), ws_endpoint(), 실시간 이벤트 — Redis pub/sub 팬아웃 (다중 워커에서도 사용자별 채널로 전달). event 형식: {"type":…, user_channel(), heartbeat(), mark_offline(), mark_online() (+24 more)

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "send_media"
Cohesion: 0.25
Nodes (9): async_sessionmaker, BackgroundTasks, UploadFile, CHAT-01: 사진·동영상은 친구 방에서만, 미성년-성인 쌍은 제한 (§4.5). 안전 분석 없이 즉시 전달(SAFE-02)하고…, send_media(), are_friends(), is_blocked_either(), AsyncSession (+1 more)

### Community 66 - "call_signaling.py"
Cohesion: 0.27
Nodes (17): call_key(), CallBusy, CallNotFound, close_call(), counterpart(), create_call(), get_call(), InvalidCallSignal (+9 more)

### Community 83 - "test_schema.py"
Cohesion: 0.29
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-…, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 84 - "Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록, Source Nodes

### Community 85 - "Q: 영상 자막 부분 기능 감사해줘"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 자막 부분 기능 감사해줘, Source Nodes

### Community 87 - "Q: ㅇㅋ 결함들 해결 방안 추천해줘"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ㅇㅋ 결함들 해결 방안 추천해줘, Source Nodes

### Community 88 - "Q: 영상 자막 결함 해결 방안 구현"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 자막 결함 해결 방안 구현, Source Nodes

### Community 89 - "v1/media.py"
Cohesion: 0.33
Nodes (7): 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., get_current_user(), AsyncSession, get_db(), get_session_factory(), 백그라운드 작업(자막·설명 부착)용 세션 팩토리. 테스트에서 override., HTTPAuthorizationCredentials

### Community 90 - "notifications.py"
Cohesion: 0.36
Nodes (9): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, BaseModel, get, ReadIn (+1 more)

### Community 108 - "conftest.py"
Cohesion: 0.11
Nodes (22): Settings, get_redis(), FastAPI 의존성. 테스트에서 override 가능하도록 분리., 소셜 OAuth 제공자 추상화 (ACC-01). - dev: OAUTH_MOCK=true → 모든 제공자 이름이 MockProvider로 동작…, BaseSettings, client(), _conn(), _force_oauth_mock() (+14 more)

### Community 116 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 117 - "scheduler.py"
Cohesion: 0.17
Nodes (15): AiStatus, description_status / caption_status 공용., get_redis_client(), 현재 이벤트 루프 전용 클라이언트. asyncio Redis 연결을 다른 루프에서 재사용하면 Future/transport가 깨지므로…, get_caption_caller(), (media_path, content_type) -> [{start,end,text}] 세그먼트. 실구현: Whisper., cleanup_stale_drafts(), APScheduler 크론 — 드래프트 청소·자막 작업 복구·SAFE 재분석. (+7 more)

### Community 118 - "vision.py"
Cohesion: 0.40
Nodes (5): generate_description(), _get_client(), AsyncOpenAI, GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드). 엔드포인트는…, 이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)

### Community 119 - "test_notifications.py"
Cohesion: 0.43
Nodes (7): _notis(), §16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증., test_comment_and_like_notify_author_not_self(), test_disabled_notification_group_is_not_stored(), test_flagged_and_restriction_notify_receiver(), test_friend_request_and_accept_notifications(), test_mark_read()

### Community 120 - "env.py"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 121 - "main.py"
Cohesion: 0.14
Nodes (14): health(), HealthOut, BaseModel, get, close_redis_client(), 현재 워커 이벤트 루프의 연결 풀을 애플리케이션 종료 시 정리한다., add_security_headers(), lifespan() (+6 more)

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 126 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 129 - "upload_video"
Cohesion: 0.12
Nodes (22): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). FE 길이는 빠른 거부용…, transcribe_voice() (+14 more)

### Community 130 - "generate_caption"
Cohesion: 0.36
Nodes (9): _cache_get(), _cache_put(), describe_image(), generate_caption(), media_hash_from_path(), AsyncSession, Path, 사진 설명 생성. 실패·한도 초과 시 None (게시·전송은 정상 유지). (+1 more)

### Community 131 - "CHAT-05 음성·영상 통화 시그널링 설계"
Cohesion: 0.29
Nodes (6): API와 이벤트, CHAT-05 음성·영상 통화 시그널링 설계, 검증, 목표와 경계, 오류 계약, 정책

### Community 132 - "media_probe.py"
Cohesion: 0.38
Nodes (6): get_video_probe(), InvalidVideo, probe_video_duration(), Exception, Path, 서버가 직접 영상 컨테이너와 재생 시간을 검증한다.

### Community 133 - "safety_model.py"
Cohesion: 0.33
Nodes (6): analyze(), AnalyzeIn, health(), BaseModel, get, safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이. 계약: POST /analyze…

### Community 134 - "RestrictionReleaseOut"
Cohesion: 0.50
Nodes (4): BaseModel, RestrictionReleaseOut, Exception, UploadTooLarge

### Community 135 - "list_messages"
Cohesion: 0.21
Nodes (25): accept_request(), create_room(), get_call(), _get_my_room(), _latest_messages(), list_messages(), list_requests(), list_rooms() (+17 more)

### Community 136 - "fake_ai"
Cohesion: 0.29
Nodes (5): CallCounter, fake_ai(), _fake_duration(), fixture, 외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints).

### Community 137 - "test_calls.py"
Cohesion: 0.53
Nodes (5): _friends_with_room(), _next_event(), CHAT-05 음성·영상 통화 — Redis 세션, 정책, WebSocket 시그널., test_call_invite_signal_lifecycle_and_participant_privacy(), test_call_rejects_restriction_invalid_role_and_oversized_signal()

## Knowledge Gaps
- **204 isolated node(s):** `thisabled-backend`, `프로젝트`, `기술 스택`, `명령어`, `DB 스키마 (v3)` (+199 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `caption_chat_message_job()` (3× useful, score=2.438030903)
- `save_upload()` (2× useful, score=1.997312493)
- `caption_post_media_job()` (2× useful, score=1.997312493)
- `caption_key()` (2× useful, score=1.997312493)
- `cleanup_stale_drafts()` (2× useful, score=1.997312493)
- `transcribe_segments()` (2× useful, score=1.997312493)
- `recommendations()` (2× useful, score=1.996372996)
- `UiMode` (2× useful, score=1.996372996)
- `user_features()` (2× useful, score=1.996372996)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `send_media`, `v1/auth.py`, `upload_video`, `users.py`, `friends.py`, `blocks.py`, `list_messages`, `v1/chat.py`, `services/chat.py`, `v1/comm.py`, `v1/media.py`, `notifications.py`, `Base`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `_Redis` connect `_Redis` to `send_media`, `v1/auth.py`, `upload_video`, `User`, `ai_media.py`, `friends.py`, `generate_caption`, `list_messages`, `call_signaling.py`, `quota.py`, `conftest.py`, `scheduler.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `StrictRequest` connect `User` to `users.py`, `v1/auth.py`, `friends.py`, `blocks.py`, `v1/chat.py`, `v1/comm.py`, `notifications.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 62 inferred relationships involving `StrictRequest` (e.g. with `HintsOut` and `PostIn`) actually correct?**
  _`StrictRequest` has 62 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `프로젝트`, `기술 스택` to the rest of the system?**
  _204 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `users.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05730238025271819 - nodes in this community are weakly interconnected._