FROM ghcr.io/astral-sh/uv:python3.13-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser && mkdir -p /app && chown -R appuser:appuser /app
USER appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appuser /app/.venv ./.venv

COPY --chown=appuser:appuser . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "main.py"]