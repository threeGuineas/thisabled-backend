# 임시 배포 — 맥미니 로컬호스팅 + Cloudflare Tunnel

개발/시연용으로 **맥미니에서 Docker Compose로 띄운 백엔드(:8000)** 를
Cloudflare Tunnel로 공개 HTTPS URL에 노출하는 가이드.
포트포워딩·고정 IP·인바운드 방화벽 개방이 필요 없다(아웃바운드 연결만 사용).

> 정식 배포 아님. 시연·프론트 연동 테스트용 임시 노출이다.

---

## 0. 사전 점검

```bash
# 백엔드가 로컬에서 떠 있는지
docker compose up -d
curl -s http://localhost:8000/api/v1/health    # {"status":"ok",...}
```

`brew` 로 cloudflared 설치:

```bash
brew install cloudflared
```

---

## 방법 A — Quick Tunnel (제일 빠름, 도메인 불필요)

URL이 매번 바뀌는 일회성 터널. "지금 30초 안에 보여줘야 함" 용.

```bash
cloudflared tunnel --url http://localhost:8000
```

출력에 `https://<랜덤>.trycloudflare.com` 이 뜬다. 이게 백엔드 공개 주소.
터미널을 닫으면 사라지고, 다시 켜면 URL이 바뀐다.

- 장점: 계정·도메인 없이 즉시
- 단점: URL 휘발성(프론트 env 매번 교체), 세션당 1개

---

## 방법 B — Named Tunnel (URL 고정, 권장)

Cloudflare에 도메인이 연결돼 있으면 `api.내도메인.com` 같은 **고정 URL**로
띄울 수 있다. 프론트 연동·시연 반복에는 이쪽이 편하다.

### B-1. 로그인 & 터널 생성

```bash
cloudflared tunnel login                    # 브라우저에서 도메인 인증
cloudflared tunnel create thisabled         # 터널 생성 → <UUID>.json 자격증명 저장
```

### B-2. 설정 파일 `~/.cloudflared/config.yml`

```yaml
tunnel: thisabled
credentials-file: /Users/ideal/.cloudflared/<UUID>.json

ingress:
  - hostname: api.내도메인.com
    service: http://localhost:8000
  - service: http_status:404
```

### B-3. DNS 라우팅 + 실행

```bash
cloudflared tunnel route dns thisabled api.내도메인.com
cloudflared tunnel run thisabled
```

이제 `https://api.내도메인.com/docs` 로 접속된다.

### B-4. (선택) 맥미니 재부팅에도 살아있게 — 서비스 등록

```bash
sudo cloudflared service install
```

---

## ⚠️ 이 앱에서 반드시 같이 바꿔야 하는 것

터널은 **HTTPS로 종단**되고, 프론트(예: `localhost:5173` 또는 Vercel)는
백엔드와 **다른 오리진(cross-site)** 이 된다. 그대로 두면 로그인은 되는데
**자동 토큰 갱신(refresh)이 깨진다.** 아래 3개를 같이 손봐야 한다.

### 1) CORS 오리진 추가 — `.env`

프론트의 실제 오리진을 넣는다. (와일드카드는 쿠키 때문에 불가)

```dotenv
CORS_ORIGINS=http://localhost:5173,https://app.내도메인.com
```

### 2) refresh 쿠키: Secure + SameSite=None  ← **핵심 함정**

refresh 토큰은 httpOnly 쿠키로 나간다. 현재 코드는 `SameSite=Lax`,
`Secure=false` 라서 **크로스사이트 fetch에서는 브라우저가 쿠키를 안 실어준다.**
→ `/auth/refresh` 가 항상 401. 크로스사이트로 쿠키를 보내려면
`SameSite=None; Secure` 가 필요하고, `None` 은 `Secure` 를 강제한다.

`.env`:
```dotenv
COOKIE_SECURE=true          # 터널은 HTTPS라 브라우저가 Secure 쿠키 허용
```

그리고 쿠키 SameSite를 환경에 따라 바꿔야 한다. `app/api/v1/auth.py`
`_set_refresh_cookie` 에서 `samesite="lax"` 를 아래처럼:

```python
samesite="none" if settings.COOKIE_SECURE else "lax",
```

> 프론트가 **백엔드와 같은 상위 도메인**(`app.내도메인.com` ↔ `api.내도메인.com`)이면
> 그래도 fetch는 cross-site 취급이라 `None;Secure` 가 안전하다.
> 프론트도 같은 호스트 경로에 함께 둘 거면 Lax로도 동작한다.

프론트 fetch는 쿠키 송수신을 위해 `credentials: "include"` 필수:
```js
fetch(`${API}/api/v1/auth/refresh`, { method: "POST", credentials: "include" })
```

### 3) SECRET_KEY 교체 — `.env`

기본값(`change-me-...`)인 채로 인터넷에 노출하면 JWT 위조 가능.

```bash
openssl rand -hex 32     # 출력값을 SECRET_KEY 에 넣기
```

변경 후 컨테이너 재시작: `docker compose up -d`

---

## 🔐 노출 시 보안 주의

- **OpenAI 비용**: 터널이 열리면 `/vision/describe`·`/stt/transcribe` 가
  인터넷에 노출된다. 인증(Bearer) 필요라 가입자만 호출 가능하지만 **가입은 공개**다.
  누가 가입→대량 호출하면 월 예산(30만원)이 샐 수 있다. 시연 끝나면 터널을 내리고,
  장기 노출이 필요하면 Cloudflare Access(이메일 인증 게이트)로 `/docs`·전 경로를 보호.
- **임시성 유지**: 시연·테스트 때만 `cloudflared` 를 켜고, 끝나면 끈다.
- **키 회전**: OpenAI 키가 외부에 노출됐다고 판단되면 대시보드에서 즉시 회전.

---

## 빠른 체크리스트

```
[ ] docker compose up -d  → /health ok
[ ] cloudflared 로 터널 기동 (방법 A 또는 B)
[ ] .env: CORS_ORIGINS 에 프론트 오리진 추가
[ ] .env: COOKIE_SECURE=true + auth.py samesite 조건부
[ ] .env: SECRET_KEY 교체 → docker compose up -d 재기동
[ ] 프론트: API_BASE = 터널 URL, fetch credentials:"include"
[ ] 시연 종료 후 터널 내리기
```
