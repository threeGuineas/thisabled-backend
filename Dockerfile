FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install --system .
# 테스트 의존성 (dev 그룹). 개발 이미지 기준 — 운영 분리 시 build arg 로 분기 예정
RUN uv pip install --system pytest==8.2.0 pytest-asyncio==0.23.6

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
