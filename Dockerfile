FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

ARG INSTALL_DEV=true
COPY pyproject.toml uv.lock ./
RUN if [ "$INSTALL_DEV" = "true" ]; then \
        uv sync --frozen --all-groups --no-install-project; \
    else \
        uv sync --frozen --no-dev --no-install-project; \
    fi

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app app
COPY --chown=app:app . .
RUN mkdir -p /app/uploads && chown app:app /app/uploads

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
