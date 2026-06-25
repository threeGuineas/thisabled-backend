# [예시] 게시글 수정 API (PUT /posts/{id})

> 이 파일은 Ralph 태스크 작성 양식 예시다. 실제로 돌려도 되는 진짜 미구현 항목.

## 배경 / 명세 출처
현재 게시글은 생성·목록·단건조회·삭제만 있고 **수정(PUT)이 없다**
(`app/api/v1/posts.py`). 소셜 피드 기능상 본인 글 수정은 필요.
명세: 게시글 CRUD (Notion 기능 목록 F0X, 본인 글만 수정 가능 — 권한 규칙은 DELETE와 동일).

## 구현 범위
- `PUT /api/v1/posts/{post_id}` 추가
- 본인 글만 수정 (타인 글 403, 없는 글 404, 미인증 401)
- 수정 가능 필드: `content`, `image_url`
- 응답: 수정된 `PostResponse`

## Definition of Done (체크리스트)
- [ ] `app/schemas/post.py`에 `PostUpdate`(content, image_url) 추가
- [ ] `app/api/v1/posts.py`에 `update_post` 핸들러 추가 (소유권 검사 DELETE와 동일 패턴)
- [ ] `tests/test_posts.py`에 테스트 추가:
  - [ ] 본인 글 수정 200 + 내용 반영 확인
  - [ ] 타인 글 수정 403
  - [ ] 없는 글 404
  - [ ] 미인증 401
- [ ] `docker compose exec -T app pytest -q` 전체 그린
- [ ] 커밋: `feat(posts): 게시글 수정 API (PUT /posts/{id})`

## 제약
- 기존 엔드포인트·스키마 시그니처를 깨지 말 것
- UUID·인증 의존성은 기존 패턴 재사용 (`get_current_user`, `uuid.UUID` path)
