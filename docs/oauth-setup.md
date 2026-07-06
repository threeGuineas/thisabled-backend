# 소셜 OAuth 실키 발급·투입·검증 가이드

dev는 `OAUTH_MOCK=true`(기본)로 키 없이 동작한다. 이 문서는 **실키 전환** 절차다.
코드 경로 자체는 `tests/test_oauth_real.py`가 MockTransport로 고정하므로,
여기서 확인할 것은 "콘솔 설정 ↔ 환경변수 ↔ 리다이렉트 URI"의 정합뿐이다.

## 0. 사전 결정: redirect URI

`OAUTH_REDIRECT_BASE`는 **브라우저가 실제로 접속하는 서버 주소**여야 한다 — "로컬 개발이니까
localhost"가 아니라 "카카오·구글 로그인 완료 후 브라우저가 리다이렉트될 수 있는 주소"가 기준이다.
Tailscale Funnel처럼 상시 배포 중이면 로컬 주소는 브라우저(카카오·구글 서버)가 도달할 수 없으므로
**Funnel 도메인을 써야 한다.**

| 환경 | OAUTH_REDIRECT_BASE | 콘솔에 등록할 URI |
|---|---|---|
| Funnel 상시 배포 (이 프로젝트 기본) | `https://<funnel-host>.ts.net` | `https://<funnel-host>.ts.net/api/v1/auth/kakao/callback`<br>`https://<funnel-host>.ts.net/api/v1/auth/google/callback` |
| 순수 로컬(Funnel 미사용, 브라우저·서버가 같은 머신) | `http://localhost:8000` | `http://localhost:8000/api/v1/auth/{provider}/callback` |

`tailscale funnel status`로 현재 Funnel 도메인을 확인한다. `.env.example`의 기본값은
범용 템플릿용 localhost이니, 실제 `.env`에는 위 표에서 실제 접속 경로에 맞는 값을 넣는다.

두 환경 모두 쓸 거면 콘솔에 URI를 **둘 다 등록**한다 (카카오·구글 모두 복수 등록 가능).

## 1. 카카오 (developers.kakao.com)

1. 내 애플리케이션 → 애플리케이션 추가 (개인 개발자, 사업자 등록 불필요)
2. 앱 설정 → 플랫폼 → **Web 플랫폼 등록**: 사이트 도메인 (`http://localhost:8000` 등)
3. 제품 설정 → **카카오 로그인 활성화** → Redirect URI 등록 (위 표)
4. 동의항목: **아무것도 켤 필요 없음** — 우리는 계정 식별자(`id`)만 쓴다
   (생년월일·닉네임은 가입 추가정보에서 직접 입력받으므로 비즈 앱 전환 불필요)
5. 앱 설정 → 앱 키 → **REST API 키** → `KAKAO_CLIENT_ID`
6. (선택) 카카오 로그인 → 보안 → Client Secret **사용** 설정 시 → `KAKAO_CLIENT_SECRET`
   - 미사용이면 비워둔다 — 코드가 파라미터 자체를 생략한다

## 2. 구글 (console.cloud.google.com)

1. 새 프로젝트 생성 → **APIs & Services → OAuth consent screen**
   - User Type: External / 앱 이름·이메일 입력 / scope 추가 불필요(openid는 기본)
   - 게시 상태 "Testing"이면 **Test users에 본인 구글 계정 추가** (미추가 시 403)
2. **Credentials → Create Credentials → OAuth client ID**
   - Application type: **Web application**
   - Authorized redirect URIs: 위 표의 google callback URI
3. Client ID → `GOOGLE_CLIENT_ID`, Client secret → `GOOGLE_CLIENT_SECRET`
   - **구글은 Web application 타입이면 secret이 항상 발급된다.** Credentials 목록에서 해당
     클라이언트를 클릭하면 다시 확인 가능. secret이 안 보인다면 Application type을 Web
     application이 아닌 다른 것(Android/iOS/Desktop 등)으로 만든 것 — 그 타입들은 서버사이드
     code 교환에 안 맞으므로 Web application으로 다시 만들어야 한다.

## 3. 환경변수 투입

`.env`에 추가 (예시는 `.env.example` 20~25행):

```bash
OAUTH_MOCK=false
KAKAO_CLIENT_ID=<REST API 키>
KAKAO_CLIENT_SECRET=            # 콘솔에서 '사용' 켰을 때만
GOOGLE_CLIENT_ID=<클라이언트 ID>
GOOGLE_CLIENT_SECRET=<클라이언트 보안 비밀>
OAUTH_REDIRECT_BASE=https://<funnel-host>.ts.net   # §0 표 참고 — localhost 아님
```

```bash
docker compose up -d app   # env 반영 재기동
```

## 4. 실검증 체크리스트

브라우저로 (curl은 제공자 로그인 페이지를 못 넘어간다):

1. `GET /api/v1/auth/kakao/authorize` 응답의 `authorize_url`을 브라우저에 붙여넣기
2. 카카오 로그인 → 콜백으로 리다이렉트 → JSON 확인
   - 신규: `is_new_user: true` + `signup_token` → Swagger에서 `POST /api/v1/auth/signup`
   - 기존: `access_token` + `refresh_token` 쿠키
3. 같은 계정으로 authorize부터 재시도 → `is_new_user: false` 즉시 로그인
4. 구글도 1~3 반복
5. 마지막으로 `OAUTH_MOCK=false` 상태에서 `docker compose exec -T app pytest -q` 그린 확인

### 자주 걸리는 오류

| 증상 | 원인 |
|---|---|
| 카카오 `KOE006` | Redirect URI 미등록 또는 오타 (스킴·포트까지 완전 일치해야 함) |
| 카카오 `KOE010` | Client Secret '사용' 상태인데 env 미설정 (또는 반대) |
| 구글 `redirect_uri_mismatch` | Authorized redirect URIs 불일치 |
| 구글 `403 access_denied` | Testing 상태에서 Test users 미등록 |
| 콜백 400 | code 만료(수 분)·재사용 — authorize부터 다시 |
| 콜백 502 | 서버가 제공자에 연결 불가 (네트워크/DNS) |
