# ThisAbled — Backend

## 프로젝트 컨텍스트
- **공모전**: 2026 한이음 드림업 (목표: 은상 이상)
- **서비스**: 장애 유형별 적응형 UI 소셜 플랫폼
  - 시각장애 모드: GPT-4o Vision 이미지 음성 해설 + Whisper 음성 댓글
  - 발달장애 모드: KoBERT 기반 그루밍/혐오 탐지 + 신고 UI
  - 청각장애 모드: 실시간 자막 + LLM 소통 코칭 (중간평가 이후)
- **팀 구성**: 프론트엔드 1 + 백엔드 1 (나) + AI 1

## 기술 스택
- **Runtime**: Python 3.11
- **Framework**: FastAPI
- **DB**: PostgreSQL 15
- **Cache**: Redis 7
- **컨테이너**: Docker Compose
- **인증**: JWT (python-jose)
- **스토리지**: S3 또는 로컬 (개발 중)
- **실시간**: WebSocket / Socket.IO (채팅용, S2에서 구현)
- **AI 연동**: GPT-4o Vision API, Whisper STT API (S2에서 구현)

## 레포 구조 (목표)
```
thisabled-backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py       # 환경변수
│   │   └── security.py     # JWT
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── posts.py
│   │       ├── users.py
│   │       └── health.py
│   ├── models/             # SQLAlchemy ORM
│   ├── schemas/            # Pydantic
│   └── db/
│       ├── session.py
│       └── init_db.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── alembic/                # DB 마이그레이션
```

## DB 스키마 (v2 — 구현 기준, F01·F02 명세 정합)
PK·FK는 전부 **UUID**. 마이그레이션: `alembic/versions/*_schema_v2_auth_mode.py`

```sql
users               -- id(uuid), nickname(12), password_hash, recovery_code_hash,
                    --   disability_mode(null=온보딩前), mode_settings(jsonb),
                    --   trust_score(=1.0), created_at, last_login_at
forbidden_nicknames -- id(serial), word(unique)   ← check-nickname 금칙어 사전(시드 22개)
user_mode_history   -- id(uuid), user_id(FK), from_mode, to_mode, changed_at
posts               -- id(uuid), user_id(FK), content, image_url, created_at
messages            -- id(uuid), sender_id(FK), receiver_id(FK), content, is_flagged, created_at
reports             -- id(uuid), reporter_id(FK), target_id(FK), reason, status, created_at
```

`disability_mode`: `visual` | `hearing` | `developmental` | `default` (NULL = 온보딩 미완료)

> 참고: `reports`는 F03 명세상 message 단위로 재설계 예정(M1). messages 안전감시 컬럼도 M1.
> ERD 산출물: `docs/erd.dbml` (dbdiagram.io)

## 현재 스프린트: S1 (5/30 ~ 6/12)
### Sprint Goal
가입 → 로그인 → 게시글 작성 → 피드 확인까지 end-to-end 동작

### 작업 목록
- [ ] FastAPI 스켈레톤 + `/health` 엔드포인트
- [ ] Docker Compose (FastAPI + PostgreSQL + Redis)
- [ ] PostgreSQL 스키마 v1 (users, posts, messages, reports)
- [ ] ERD 다이어그램 (dbdiagram.io DSL 또는 drawio XML)
- [ ] JWT 인증 미들웨어 (회원가입 / 로그인 API)
- [ ] 게시글 CRUD API
- [ ] 이미지 업로드 (S3 또는 로컬 스토리지)
- [ ] 서비스 구성도 작성 (보고서용 아키텍처 다이어그램)

### Definition of Done (S1)
- 사용자가 가입 후 게시글 1개 작성하고 피드에서 볼 수 있음
- 3개 장애 모드 토글이 백엔드 응답에 반영됨 (프론트 연동 기준)
- Docker Compose `up` 한 번으로 전체 환경 실행

## 데드라인
```
6/12  S1 마감 — 가입→피드 동작
6/23  중간평가 시작
7/14  ⚠️ 중간평가 마감 (영상 + 보고서 + SW 설계서 7종)
10/30 🎯 최종 제출 마감
```

## 중간평가 산출물 중 백엔드 담당
| 산출물 | 도구 | 마감 |
|--------|------|------|
| ERD | dbdiagram.io 또는 drawio | S1 (6/12) |
| 서비스 구성도 | drawio | S1 (6/12) |
| 기능 처리도 | drawio | S2 (6/26) |
| 핵심 소스코드 발췌 | 직접 | M1 (7/14) |

## 리스크 & 주의사항
- **GPT-4o API 비용**: 캐싱 필수 (Redis, 동일 이미지 중복 호출 방지). 월 예산 30만원.
- **그루밍 탐지 모델**: AI 팀 KoBERT 결과를 `/api/v1/moderation` 엔드포인트로 연동 예정
- **WebSocket 채팅**: S2부터 구현. S1에서는 REST API만.
- **복지카드 OCR**: 후순위 (9/5까지 미동작 시 컷)

## 협업 규칙
- 블로커는 디스코드 #blockers에 즉시 공유
- PR은 24시간 내 리뷰 응답
- 결정사항은 ADR(Architecture Decision Record)로 노션에 기록

## 개발 워크플로우 (Claude Code)

### 브랜치 전략 — 워크트리 모델 (Superpowers)
`main` 단일 통합 브랜치. feature는 **격리된 git worktree**에서 작업한다.
- **기능 착수 시**: `using-git-worktrees` 스킬로 격리 워크스페이스 생성
  (현재 작업트리를 더럽히지 않고 병렬 작업 가능)
- **완료 시**: `finishing-a-development-branch` 스킬로 테스트 통과 검증 →
  main 병합 또는 PR 생성 → 워크트리 정리
- 단, **셋업·문서·설정 변경처럼 작은 단일 작업은 main에서 직접** 진행 가능
- main은 항상 `pytest` 그린 상태 유지

### 커밋 시점·단위
- **1 논리 변경 = 1 커밋** (기능/수정/리팩터를 한 커밋에 섞지 않는다)
- **테스트가 통과한 뒤에만 커밋** (`docker compose exec -T app pytest -q` 그린)
- **Ralph 루프 모드에서는 1 태스크 = 1 커밋** (태스크 완료마다 커밋)
- 커밋 메시지는 아래 `커밋 메시지 규칙` 준수

### 테스트 실행
```bash
docker compose exec -T app pytest -q       # 전체
docker compose exec -T app pytest tests/test_auth.py -q   # 파일 단위
```
신규 엔드포인트·스키마 변경 시 대응 테스트를 같은 커밋에 포함한다.

## 커밋 메시지 규칙

Conventional Commits 기반. 형식: `<type>(<scope>): <subject>`

| type | 용도 |
|------|------|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `chore` | 빌드·설정·패키지 (기능 변화 없음) |
| `refactor` | 동작 변경 없는 코드 개선 |
| `docs` | 문서·주석만 변경 |
| `test` | 테스트 추가·수정 |
| `ci` | CI/CD 파이프라인 |

**scope** (선택): `auth` / `posts` / `users` / `messages` / `reports` / `db` / `infra` / `ai`

**규칙**
- subject는 명령형 현재형, 50자 이내 (한글 가능)
- 본문이 필요한 경우 빈 줄 후 72자 줄바꿈
- 본문에 `Why:` / `How:` 로 의사결정 맥락 기록
- 스프린트 관련 커밋은 subject 끝에 `[S1]` 태그

**예시**
```
chore(infra): Docker Compose 환경 초기 구성 [S1]
feat(auth): JWT 로그인 / 회원가입 API 구현 [S1]
fix(posts): 이미지 없을 때 500 에러 수정
refactor(db): async session 팩토리 단일화
```

## 관련 링크
- 노션 프로젝트: https://www.notion.so/61acd58764108252bcfb8111ff879042
- 실행 계획서: https://www.notion.so/761cd5876410837c91c1019dba320034