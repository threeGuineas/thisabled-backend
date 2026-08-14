# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 122 files · ~60,749 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1207 nodes · 2762 edges · 138 communities (85 shown, 53 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 187 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `11ddf6f3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- users.py
- posts.py
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- generate_caption
- register
- test_safe.py
- GoogleProvider
- quota.py
- match_model.py
- test_ws.py
- v1/auth.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_oauth_real.py
- models/user.py
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- v1/chat.py
- test_comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- conftest.py
- 11. AI 안심 채팅
- 1. 서비스 개요
- v1/media.py
- 4. 사용자 정책
- 10. 1:1 채팅
- 12. 시각장애인 모드
- main.py
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
- _Redis
- datetime
- SAFE 그루밍 평가 결과
- relations.py
- test_media.py
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
- test_notifications.py
- Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록
- Q: 영상 자막 부분 기능 감사해줘
- thisabled-backend
- Q: ㅇㅋ 결함들 해결 방안 추천해줘
- Q: 영상 자막 결함 해결 방안 구현
- stt.py
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
- test_auth.py
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- oauth.py
- test_friends.py
- test_age.py
- env.py
- validate_nickname
- FakeMatch
- Chat Read Status Implementation Plan
- test_schema.py
- async_sessionmaker
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- try_consume
- AsyncSession
- v1/comm.py
- BackgroundTasks
- delete
- get
- patch
- Any
- FastAPI

## God Nodes (most connected - your core abstractions)
1. `User` - 64 edges
2. `register()` - 39 edges
3. `auth_header()` - 36 edges
4. `_post()` - 33 edges
5. `_Redis` - 32 edges
6. `send_media()` - 26 edges
7. `ChatMessage` - 26 edges
8. `PostCategory` - 23 edges
9. `Base` - 23 edges
10. `ThisAbled 기능 명세서 v2.2` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_processing_draft_excluded_from_feed()` --calls--> `Post`  [EXTRACTED]
  tests/test_posts.py → app/models/post.py
- `test_photo_post_gets_description_on_publish()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_vision_quota_exceeded_publishes_without_description()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py

## Import Cycles
- None detected.

## Communities (138 total, 53 thin omitted)

### Community 0 - "User"
Cohesion: 0.19
Nodes (27): accept_request(), _author(), create_room(), _get_my_room(), list_messages(), list_requests(), list_rooms(), _message_out() (+19 more)

### Community 1 - "users.py"
Cohesion: 0.14
Nodes (38): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+30 more)

### Community 2 - "posts.py"
Cohesion: 0.09
Nodes (68): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), _contains_pattern(), create_comment(), create_post(), delete_comment() (+60 more)

### Community 3 - "ai_media.py"
Cohesion: 0.11
Nodes (31): content_type_from_path(), STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다., _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job(), describe_post_media_job(), file_path_from_url() (+23 more)

### Community 5 - "friends.py"
Cohesion: 0.08
Nodes (49): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, get, accept_request(), _author() (+41 more)

### Community 6 - "generate_caption"
Cohesion: 0.52
Nodes (7): _cache_get(), _cache_put(), describe_image(), generate_caption(), AsyncSession, 사진 설명 생성. 실패·한도 초과 시 None (게시·전송은 정상 유지)., 자막 세그먼트 생성. 쿼터는 업로드 시점에 이미 차감 — 실패(재시도 소진) 시 복원.

### Community 7 - "register"
Cohesion: 0.18
Nodes (29): auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), test_chat_video_gets_caption_and_notifies_both_users() (+21 more)

### Community 8 - "test_safe.py"
Cohesion: 0.35
Nodes (11): _send(), _friend_room(), SAFE-01~05 — 동기 분석·블러·내용 보기·성능저하 모드·관계 단위 전송 제한., §18.3: 복구 후 재분석 — flagged면 소급 블러 + 수신자 알림., 수신자가 '내용 보기'를 실행한 메시지도 누적 집계에 포함 (SAFE-05-6)., test_block_overrides_restriction(), test_degraded_mode_friend_vs_request(), test_flagged_message_blurred_until_reveal() (+3 more)

### Community 9 - "GoogleProvider"
Cohesion: 0.08
Nodes (11): GoogleProvider, _http(), KakaoProvider, MockProvider, OAuthProvider, OAuthUserInfo, AsyncClient, Protocol (+3 more)

### Community 10 - "quota.py"
Cohesion: 0.16
Nodes (24): caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자·서비스 전체 호출 한도. 키는 날짜/분 단위로 자연…, 내부 재시도도 실제 STT 1회이므로 서비스 전체 상한에 추가 반영한다. (+16 more)

### Community 11 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 12 - "test_ws.py"
Cohesion: 0.14
Nodes (14): user_channel(), FakeSafety, fixture, 돈' 포함 → flagged. fail=True → SafetyUnavailable (§18.3)., safety(), fixture, safety(), fixture (+6 more)

### Community 13 - "v1/auth.py"
Cohesion: 0.11
Nodes (37): authorize(), callback(), _frontend_redirect(), logout(), AsyncSession, get, UUID, ACC-01/02 — 소셜 OAuth 전용 인증. 흐름: authorize → 제공자 로그인 → callback → FRONTEND_URL로… (+29 more)

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics(), load_cases() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.2)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~03 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 18 - "test_oauth_real.py"
Cohesion: 0.13
Nodes (18): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), _google_transport(), _kakao_transport(), fixture, 실 제공자(카카오·구글) OAuth 경로 — 외부 API를 MockTransport로 대체해 검증. 실키 없이 코드 경로(파라미터 인코딩·토큰… (+10 more)

### Community 19 - "models/user.py"
Cohesion: 0.11
Nodes (26): delete, UUID, BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거., remove_block(), AsyncSession, BaseModel, get, RecommendationListOut (+18 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "v1/chat.py"
Cohesion: 0.14
Nodes (21): BaseModel, CHAT-01/02/03 — 1:1 채팅 · 요청함 · SAFE-03 블러 · SAFE-05 제한 해제., RestrictionReleaseOut, AiStatus, description_status / caption_status 공용., §CHAT-02 — request=요청함, active=일반 채팅., RoomState, Exception (+13 more)

### Community 23 - "test_comm.py"
Cohesion: 0.06
Nodes (25): _collect_strings(), CommUnavailable, get_comm_client(), OpenAICommClient, _plain_text(), COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상). 버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개…, FastAPI 의존성 — 테스트에서 fake로 override., 외부 코칭 결과를 안전한 API 응답으로 만들 수 없을 때. (+17 more)

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

### Community 30 - "conftest.py"
Cohesion: 0.18
Nodes (13): _BorrowedSession, client(), _conn(), _force_oauth_mock(), AsyncClient, fixture, 테스트 공용 픽스처. 각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`…, .env의 실키·OAUTH_MOCK=false는 배포용 — 테스트는 항상 mock 제공자로 결정론적으로 실행한다. 개별… (+5 more)

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 33 - "v1/media.py"
Cohesion: 0.08
Nodes (37): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). FE 길이는 빠른 거부용… (+29 more)

### Community 34 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 35 - "10. 1:1 채팅"
Cohesion: 0.40
Nodes (5): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설)

### Community 36 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 37 - "main.py"
Cohesion: 0.10
Nodes (26): Any, health(), HealthOut, BaseModel, get, lifespan(), FastAPI, _add_error_response() (+18 more)

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
Cohesion: 0.10
Nodes (39): ChatReadState, ChatRoom, SAFE-05 관계 단위 자동 전송 제한. 누적 카운터는 별도 컬럼 없이 chat_messages에서 `flagged AND…, 1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅. 참여자는 정규화 쌍(user_a < user_b,…, SendRestriction, advance_read_cursor(), ChatPolicyError, counterpart_id() (+31 more)

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

### Community 54 - "_Redis"
Cohesion: 0.17
Nodes (7): _Connection, _Engine, Exception, 헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다., _Redis, test_health_degraded_is_503_and_hides_exception(), test_health_ok()

### Community 55 - "datetime"
Cohesion: 0.22
Nodes (12): Base, _utcnow(), AiResultCache, 동일 미디어 해시 캐싱 (VISION-01·CAPTION-01 중복 호출 방지, 비용 방어)., Block, 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거., ForbiddenNickname, 운영자 관리 금칙어 사전 (ACC-01 닉네임 정책). (+4 more)

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "relations.py"
Cohesion: 0.24
Nodes (13): normalize_pair(), UUID, 사용자 쌍 정규화. friendships·chat_rooms는 (작은 UUID, 큰 UUID) 순으로 저장한다., get_or_create_room(), 친구=active, 비친구=request. 차단·수신 거부·미성년 보호는 사유 비노출로 거부., are_friends(), block_user(), is_blocked_either() (+5 more)

### Community 66 - "test_media.py"
Cohesion: 0.08
Nodes (20): get_video_probe(), InvalidVideo, probe_video_duration(), Exception, Path, 서버가 직접 영상 컨테이너와 재생 시간을 검증한다., CallCounter, fake_ai() (+12 more)

### Community 83 - "test_notifications.py"
Cohesion: 0.48
Nodes (6): _notis(), §16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증., test_comment_and_like_notify_author_not_self(), test_flagged_and_restriction_notify_receiver(), test_friend_request_and_accept_notifications(), test_mark_read()

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

### Community 89 - "stt.py"
Cohesion: 0.09
Nodes (24): Settings, _extract_audio_to_m4a(), _get_client(), AsyncOpenAI, Path, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막). 엔드포인트는 `stt.transcribe(...)` 를…, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 최대 200MB 영상을 STT 상한 안의 단일 채널 M4A 음성으로 정규화한다. (+16 more)

### Community 90 - "notifications.py"
Cohesion: 0.32
Nodes (11): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, BaseModel, get, ReadIn (+3 more)

### Community 108 - "test_auth.py"
Cohesion: 0.29
Nodes (11): ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_refresh_rotates_access_token(), test_rejoin_blocked_within_30_days(), test_signup_duplicate_nickname(), test_signup_forbidden_nickname(), test_signup_minor_blocks_stranger_requests() (+3 more)

### Community 116 - "oauth.py"
Cohesion: 0.27
Nodes (8): §15: 탈퇴 후 30일 재가입 제한 판정용. users 행은 hard delete하고 여기에만 흔적., WithdrawnSocial, get_provider(), 소셜 OAuth 제공자 추상화 (ACC-01). - dev: OAUTH_MOCK=true → 모든 제공자 이름이 MockProvider로 동작…, AsyncSession, §15 회원 탈퇴. - 계정·프로필 즉시 삭제 (users hard delete) - 게시물·댓글: 사용자가 익명화/삭제 선택 - 채팅…, withdraw(), PostsAction

### Community 117 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 118 - "test_age.py"
Cohesion: 0.33
Nodes (8): age_band(), MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다., date, 만 나이·연령대·쌍 정규화 유틸 (§4.5, MATCH-02-5)., test_age_band_boundaries(), test_full_age_boundaries(), test_is_minor_range(), test_normalize_pair_orders_by_uuid()

### Community 119 - "env.py"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 120 - "validate_nickname"
Cohesion: 0.40
Nodes (4): AsyncSession, 닉네임 정책 (ACC-01): 2~12자 한글·영문·숫자, 금칙어·중복 불가., 형식(400) → 금칙어(400) → 중복(409) 순 검증. 통과 시 None., validate_nickname()

### Community 121 - "FakeMatch"
Cohesion: 0.40
Nodes (3): FakeMatch, match(), fixture

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 124 - "test_schema.py"
Cohesion: 0.29
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-…, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 129 - "try_consume"
Cohesion: 0.29
Nodes (8): consume_vision(), 일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백., 카운터 1 증가. 한도 초과면 롤백 후 False., CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원., refund(), try_consume(), test_refund_restores_slot(), test_try_consume_respects_limit()

### Community 131 - "v1/comm.py"
Cohesion: 0.15
Nodes (33): _coach(), complete(), hints(), HintsOut, _post_context(), PostIn, AsyncSession, BaseModel (+25 more)

## Knowledge Gaps
- **198 isolated node(s):** `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)`, `media (VISION-01 · CAPTION-01 · VIS-03)`, `friends / blocks (FRIEND-01/02 · BLOCK-01)` (+193 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **53 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `caption_chat_message_job()` (3× useful, score=2.43951839)
- `save_upload()` (2× useful, score=1.998531089)
- `caption_post_media_job()` (2× useful, score=1.998531089)
- `caption_key()` (2× useful, score=1.998531089)
- `cleanup_stale_drafts()` (2× useful, score=1.998531089)
- `transcribe_segments()` (2× useful, score=1.998531089)
- `recommendations()` (2× useful, score=1.997591019)
- `UiMode` (2× useful, score=1.997591019) _(code changed — re-verify)_
- `user_features()` (2× useful, score=1.997591019)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `relations.py`, `v1/media.py`, `posts.py`, `v1/comm.py`, `users.py`, `friends.py`, `services/chat.py`, `v1/auth.py`, `models/user.py`, `oauth.py`, `datetime`, `notifications.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `_post()` connect `friends.py` to `User`, `v1/media.py`, `v1/comm.py`, `match_model.py`, `v1/auth.py`, `notifications.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `_Redis` connect `_Redis` to `User`, `v1/media.py`, `try_consume`, `ai_media.py`, `friends.py`, `generate_caption`, `quota.py`, `v1/chat.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)` to the rest of the system?**
  _198 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `users.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13846153846153847 - nodes in this community are weakly interconnected._
- **Should `posts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09070714550166604 - nodes in this community are weakly interconnected._