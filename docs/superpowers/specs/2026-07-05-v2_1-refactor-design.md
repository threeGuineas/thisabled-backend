# ThisAbled 백엔드 v2.1 전면 리팩토링 — 설계

- 작성일: 2026-07-05
- 기준 명세: `docs/ThisAbled_기능명세서_v2_1.md` (SSOT)
- 목표: 중간평가(7/14)까지 설계 산출물 4종 + 백엔드 코드를 v2.1 정합으로 전면 갱신

## 0. 확정된 결정

| 결정 | 내용 |
| --- | --- |
| 우선순위 | 문서와 코드 동시 전면 리팩토링 |
| DB 전략 | 기존 마이그레이션 폐기, **v3 단일 baseline** 마이그레이션 + DB drop & recreate (실사용자 데이터 없음) |
| OAuth | **mock 제공자로 먼저 개발**, 카카오/구글 실키는 발급 후 환경변수만 교체해 별도 확인. 생년월일은 제공자가 아닌 가입 추가정보 화면에서 직접 입력받으므로 카카오 비즈 앱 전환 불필요 |
| 채팅 실시간 | **WebSocket 포함** (FastAPI WS + Redis pub/sub) |
| AI 모델 경계 | SAFE·MATCH는 **별도 모델 서버 HTTP** (AI 팀원 담당). 지금은 compose의 mock 서비스로 대체 |
| 문서 형식 | erd.dbml + drawio 유지, API 요약은 `docs/api.md` 신규 (정본은 FastAPI OpenAPI) |
| 실행 방식 | **B. 스키마 빅뱅**: baseline 스키마 전체 → 문서 → API 병렬 구현. `feature/v2_1-refactor` 브랜치 1개, 도메인별 1커밋, 완료 시 PR 1개 |
| 신고(reports) | MVP 제외 — 테이블·코드 제거 |

## 1. DB 스키마 v3 (baseline)

PK·FK 전부 UUID 유지. 기존 6개 테이블 → 아래로 재편.

### 계정·프로필

- **users** — id, nickname(unique, 2~12자), **birth_date**(만 나이·연령대·미성년 여부는 저장하지 않고 요청 시 서버 계산), **ui_mode**(`visual|hearing|developmental` — v2.1에 'default' 없음, `disability_mode`에서 개명 §18.3), bio(≤300자), profile_image_url, stranger_requests_allowed(가입 시 성인 true / 미성년 false 초기화, 본인 변경 가능 §4.5), mode_settings(jsonb — 글자 크기·대비·자막 설정), risk_score(SAFE-04 내부 점수), created_at, last_login_at
  - `password_hash`·`recovery_code_hash`·`trust_score` 제거
- **social_identities** — user_id FK, provider(`kakao|google|mock`), provider_user_id, unique(provider, provider_user_id)
- **withdrawn_socials** — provider, provider_user_id, withdrawn_at. 탈퇴 후 **30일 재가입 제한** 판정(§15). users 행은 탈퇴 시 hard delete
- **interest_tags** — TAG-01 카탈로그 시드(10 카테고리 41개 태그) / **user_interest_tags** — user_id+tag_id unique, 최대 10개는 앱 검증
- **forbidden_nicknames**, **user_mode_history** — 유지

### 게시물

- **posts** — id, author_id(**nullable** — 탈퇴 익명화 SET NULL='탈퇴한 사용자'), content, **status(`processing|published`)**, published_at, created_at, updated_at
  - 텍스트·사진: 생성 즉시 published. 영상: 업로드 시점에 processing 내부 드래프트 생성(POST-01), 게시 실행 시 published, 24시간 미게시 시 자동 삭제(CAPTION-01)
  - 명세의 `작성 중` 상태는 서버 레코드가 생기기 전(클라이언트 편집 중)이므로 DB 상태로 두지 않음. 자막 완료 후 미게시 드래프트는 processing + caption_status=done으로 구분
- **post_media** — post_id, media_type(`image|video`), url, sort_order(사진≤3, 영상 1개는 앱 검증), media_hash, description(+description_status — VISION), caption jsonb(+caption_status `processing|done|failed|none` — CAPTION)
- **comments** — post_id, author_id(nullable), content, created_at, updated_at
- **post_likes** — (post_id, user_id) 복합 PK

### 관계

- **friend_requests** — sender_id, receiver_id, status(`pending|accepted|declined|cancelled`), responded_at(거절 후 30일 추천 제외 판정 MATCH-03)
- **friendships** — (user_a, user_b) 정규화 쌍(작은 UUID가 a), unique
- **blocks** — blocker_id, blocked_id, unique 쌍. 차단 시 친구 관계 해제 + 채팅 차단(BLOCK-01)

### 채팅·SAFE

- **chat_rooms** — (user_a, user_b) unique 쌍, state(`request|active`), requested_by, accepted_at
  - 비친구 첫 메시지 → request 상태 방 생성(수락 전 텍스트 1건만, CHAT-02), 수락 시 active. 친구 간 시작은 즉시 active
- **chat_messages** — room_id, sender_id(nullable — 탈퇴 익명화), type(`text|image|video`), content, media_url, description(+status), caption(+status), **safety_status(`pending|safe|flagged|unanalyzed`)**, revealed_at('내용 보기' 실행 시각 — 집계 포함 근거 SAFE-05-6), created_at
- **send_restrictions** — sender_id, receiver_id, active, created_at, released_at
  - SAFE-05 집계: `chat_messages`에서 `flagged AND created_at > max(now-3일, 마지막 released_at)` 카운트 쿼리(별도 카운터 컬럼 없음 → 해제=released_at 경계=리셋). 기간·횟수는 설정값

### 기타

- **notifications** — user_id, type, payload jsonb, read_at, created_at (§16 유형 전부)
- **ai_result_cache** — kind(`vision|caption`), media_hash, result jsonb, unique(kind, media_hash) (동일 해시 중복 호출 방지)
- 호출 한도 카운터는 Redis TTL 키: vision 20/일·5/분(이미지 1장=1회, 게시물·채팅 합산), caption 5/일. 자막 실패(재시도 소진) 시 횟수 복원, 24h 드래프트 삭제 시 복원 없음(CAPTION-01)

## 2. 아키텍처

```
FE (React PWA)
  │ HTTPS(REST) + WSS
  ▼
app (FastAPI) ──── db (PostgreSQL 15)
  │    │      └── redis (캐시·쿼터·pub/sub)
  │    ├─ HTTP → safety-model 서비스 (자체 안전 모델 — 현재 mock 컨테이너)
  │    ├─ HTTP → match-model 서비스 (SBERT+LightGBM — 현재 mock 컨테이너)
  │    └─ HTTPS → 외부 AI API (Whisper STT / 이미지 설명 / COMM LLM) — §17 고지 대상
```

- **WebSocket**: `/ws` 단일 엔드포인트, Redis pub/sub 경유 팬아웃(다중 워커 대비). 새 메시지·알림 푸시
- **백그라운드**: 자막·사진설명 생성은 asyncio 태스크(상태는 DB), 24h 드래프트 청소·미분석 재분석은 APScheduler 인프로세스 크론. 별도 워커 컨테이너 없음(MVP 규모)
- **장애 대응(§18.3)**: safety-model 타임아웃/장애 시 — 친구 텍스트는 `unanalyzed`로 전달(성능저하 모드), 비친구 요청은 `pending` 보류. 복구 후 재분석 → flagged면 소급 블러 + 알림. 미분석을 `정상` 표시 금지
- compose 서비스: `app` `db` `redis` `safety-model`(mock) `match-model`(mock)

## 3. API 표면 (v1)

| 그룹 | 주요 엔드포인트 | 비고 |
| --- | --- | --- |
| auth | `GET /auth/{provider}/authorize` → `GET /auth/{provider}/callback` → 기가입자 토큰 발급 / 신규는 단기 **signup_token** → `POST /auth/signup` / refresh / logout | signup에서 만14세·30일 재가입·닉네임 검증. 제공자 추상화(Kakao/Google/Mock), env 토글 |
| users | me, 프로필 수정(자기소개 연락처 패턴 검증 MATCH-02-7), 태그, 설정(모드 변경→history, stranger_requests_allowed), 탈퇴(게시물 익명화/삭제 선택, unlink, withdrawn_socials 기록) | |
| posts/feed | 피드 커서 페이지네이션(published만, 차단 제외), CRUD, 미디어 업로드(영상=드래프트+자막 시작), publish, 좋아요, 댓글 | VISION은 게시 시점 생성(§VISION-01) |
| friends/blocks | 요청 생성/취소/수락/거절, 친구 목록/해제, 차단/해제 | |
| recommendations | `GET /recommendations` — 후보 풀·제외조건(차단/친구/거절30일/미성년↔성인)은 **백엔드 강제**, 점수·사유만 match-model | UI 모드 비노출(MATCH-04) |
| chat | 방 목록/요청함, 메시지 전송(SAFE 동기 → flagged 블러 저장·전달 → SAFE-05 체크·제한 발동), 내용 보기, 제한 해제(수신자), 미디어 전송(친구만+미성년-성인 제한, 즉시 전달 후 설명/자막 비동기 부착) | 제한된 발신자에겐 사유 비노출(SAFE-05-4, CHAT-02) |
| comm | simplify / complete / suggest-replies / hints | 버튼 실행 시에만, 최근 N=10 메시지. 키 없으면 stub |
| notifications | 목록/읽음 | WS 푸시 병행 |
| ws | `/ws` | 토큰 인증 |

기존 `stt`·`vision`·`upload` 엔드포인트는 위 구조로 재배치.

## 4. 문서 산출물

1. `docs/erd.dbml` — §1 반영
2. `docs/architecture.drawio` — §2 반영 재작성
3. `docs/function-flow.drawio` — 핵심 흐름 5개: 가입(OAuth), 영상 게시물 수명주기, 채팅 SAFE 파이프라인(+SAFE-05), 비친구 요청함, 차단/탈퇴
4. `docs/api.md` — 신규, §3 요약표
5. `CLAUDE.md` — 스키마 정본·테이블 목록·enum 갱신, reports 문구 제거

## 5. 테스트 전략

- 도메인별 pytest: test_auth / test_users / test_posts / test_friends / test_chat / test_safe / test_comm / test_notifications
- 외부 AI·모델 서비스는 DI로 fake 주입(HTTP mock). WS는 TestClient
- 완료 기준: `docker compose exec -T app pytest -q` 그린

## 6. 구현 순서 (빅뱅)

1. baseline 마이그레이션 + SQLAlchemy 모델 전체 + 시드(태그·금칙어)
2. 문서 4종 + CLAUDE.md 갱신
3. API 구현 커밋 순서: auth·users → posts·feed·미디어 → friends·blocks → chat REST + SAFE → WebSocket → notifications·탈퇴 → comm·recommendations(stub)
4. 시간 부족 시 절단 가능 지점: WebSocket 이후(→REST 폴링으로 시연), comm·recommendations(stub 응답이므로 마지막)

## 7. 명세와의 정합 노트 (구현 설계에서 확정한 값)

- 닉네임 허용 문자: 한글·영문·숫자 (v2 정책 유지, §ACC-01 위임사항)
- SAFE 동기 분석 타임아웃: 2초 (초과 시 §18.3 성능저하 모드)
- COMM 최근 메시지 N=10 (§COMM-05 초기값)
- 연령대 구간: §MATCH-02-5의 6구간을 서버 상수로
- SAFE-05 기간 3일·횟수 3회, VISION/CAPTION 한도: 환경변수 설정값
