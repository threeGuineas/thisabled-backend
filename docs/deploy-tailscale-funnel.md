# 임시 배포 — 맥미니 로컬호스팅 + Tailscale Funnel

맥미니에서 Docker Compose로 띄운 백엔드(:8000)를 **Tailscale Funnel**로
공개 HTTPS URL에 노출하는 가이드. Cloudflare Quick Tunnel과 달리
**URL이 고정**된다(`https://<머신명>.<tailnet>.ts.net`), 별도 도메인 구매도 불필요.

> 정식 배포 아님. 시연·프론트 연동 테스트용 임시 노출이다.
> Cloudflare Tunnel 가이드는 [deploy-tunnel.md](./deploy-tunnel.md) 참고(그대로 유지).

---

## 0. 사전 점검

```bash
docker compose up -d
curl -s http://localhost:8000/api/v1/health    # {"status":"ok",...}
```

---

## 1. Tailscale 설치 & 로그인

```bash
brew install tailscale
sudo tailscale up
```

브라우저가 열리며 Tailscale 계정(Google/GitHub 등)으로 로그인 → 이 맥미니가
tailnet(개인 사설망)에 등록된다. 등록되면 머신 이름이 정해진다
(`tailscale status`로 확인, 예: `mac-mini`).

## 2. Funnel 기능 켜기 (최초 1회, 콘솔에서)

Tailscale 관리 콘솔(https://login.tailscale.com/admin/acls) → **DNS / HTTPS**
탭에서 **HTTPS Certificates** 활성화 + **Funnel** 기능을 tailnet에서 허용.
(개인 tailnet은 기본적으로 둘 다 무료로 켤 수 있다.)

## 3. Funnel 실행

```bash
sudo tailscale funnel 8000
```

출력에 고정 URL이 뜬다:
```
https://mac-mini.<tailnet-name>.ts.net
```

이 URL이 백엔드 공개 주소다. **머신명이 바뀌지 않는 한 URL은 영구적으로 고정**된다
— 매번 터널을 새로 켜도 동일 URL 유지(Cloudflare Quick Tunnel과의 핵심 차이).

```bash
curl -s https://mac-mini.<tailnet-name>.ts.net/api/v1/health
```

종료는 `Ctrl+C` 또는:
```bash
sudo tailscale funnel --bg=false 8000   # 포그라운드 종료
tailscale funnel status                  # 현재 노출 상태 확인
```

### 백그라운드로 + 재부팅에도 유지

```bash
sudo tailscale funnel --bg 8000
```

---

## ⚠️ 이 앱에서 반드시 같이 바꿔야 하는 것

Tailscale Funnel도 결국 **HTTPS 종단 + 프론트와 크로스오리진**이라는 점은
Cloudflare Tunnel과 동일하다. 아래는 이미 코드에 반영되어 있다/해야 한다.

### 1) refresh 쿠키 SameSite — 이미 반영됨 ✅

`app/api/v1/auth.py`의 `_set_refresh_cookie`는
`samesite="none" if settings.COOKIE_SECURE else "lax"`로 분기되어 있다
([auth.py](../app/api/v1/auth.py)). **`.env`에서 `COOKIE_SECURE=true`만 켜면**
크로스오리진 refresh가 정상 동작한다.

### 2) `.env` 설정

```dotenv
COOKIE_SECURE=true
CORS_ORIGINS=http://localhost:5173,https://app.내도메인.com
SECRET_KEY=<openssl rand -hex 32 로 생성한 값>
```

변경 후:
```bash
docker compose up -d
```

### 3) 프론트 fetch

```js
fetch(`${API}/api/v1/auth/refresh`, { method: "POST", credentials: "include" })
```

---

## Cloudflare Tunnel과 비교

| | Cloudflare Quick Tunnel | Cloudflare Named Tunnel | **Tailscale Funnel** |
|---|---|---|---|
| URL 고정 | ❌ 매번 랜덤 | ✅ (도메인 보유 시) | ✅ (계정만 있으면) |
| 도메인 구매 필요 | ❌ | ✅ | ❌ |
| 설정 난이도 | 최소 | 중간(DNS 라우팅) | 낮음 |
| 인바운드 방화벽 개방 | 불필요 | 불필요 | 불필요 |

---

## ⚠️ 노출 시 보안 주의 (Cloudflare 가이드와 동일)

- `/vision/describe`·`/stt/transcribe`는 가입자라면 누구나 호출 가능 → OpenAI
  월 예산(30만원) 소진 위험. 시연 끝나면 `tailscale funnel` 끄기.
- 장기 노출이 필요하면 Tailscale ACL로 특정 사용자/디바이스만 Funnel 접근 허용하거나,
  애초에 Funnel 대신 tailnet 내부 공유(같은 tailnet 기기끼리만)로 전환 검토.
- OpenAI 키가 외부에 노출됐다고 판단되면 대시보드에서 즉시 회전.

---

## 빠른 체크리스트

```
[ ] docker compose up -d → /health ok
[ ] tailscale up (최초 1회 로그인)
[ ] 관리 콘솔에서 HTTPS Certificates + Funnel 활성화 (최초 1회)
[ ] sudo tailscale funnel 8000  (또는 --bg)
[ ] .env: COOKIE_SECURE=true, CORS_ORIGINS, SECRET_KEY 교체 → docker compose up -d
[ ] 프론트: API_BASE = https://<머신명>.<tailnet>.ts.net, fetch credentials:"include"
[ ] 시연 종료 후 funnel 끄기 (`tailscale funnel --bg=false 8000` 또는 콘솔에서 비활성화)
```
