FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY src ./src
COPY run.py ./run.py

FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src
COPY --from=builder /app/run.py ./run.py

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "run.py"]