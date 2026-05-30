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

## DB 스키마 (v1 목표)
핵심 테이블 4개:

```sql
users       -- id, nickname, password_hash, disability_type, created_at
posts       -- id, user_id(FK), content, image_url, created_at
messages    -- id, sender_id(FK), receiver_id(FK), content, is_flagged, created_at
reports     -- id, reporter_id(FK), target_id(FK), reason, status, created_at
```

`disability_type`: `visual` | `developmental` | `hearing` | `none`

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
- 브랜치 전략: `main` / `develop` / `feature/*`
- PR은 24시간 내 리뷰 응답
- 블로커는 디스코드 #blockers에 즉시 공유
- main 브랜치는 CI 통과 후 머지
- 결정사항은 ADR(Architecture Decision Record)로 노션에 기록

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