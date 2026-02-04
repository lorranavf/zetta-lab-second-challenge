FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/app/.cache/uv \
    UV_LINK_MODE=copy

WORKDIR /app

RUN adduser --disabled-password --gecos "" --home "/app" --shell "/sbin/nologin" --no-create-home --uid 1000 app
RUN mkdir -p /app/.cache/uv && chown -R app:app /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/app/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --extra api

ARG INSTALL_TEST=false

RUN --mount=type=cache,target=/app/.cache/uv \
    if [ "$INSTALL_TEST" = "true" ] ; then \
    uv sync --frozen --no-install-project --all-extras; \
    fi

RUN chown -R app:app /app

USER app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
