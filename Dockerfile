# ================================
# 🧱 Stage 1: Backend build
# ================================
FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS backend-builder
WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen && uv pip install uvicorn --no-cache-dir

COPY backend/src ./src
COPY backend/run_api.py ./run_api.py

RUN uv run playwright install --with-deps chromium


# ================================
# 🧱 Stage 2: Frontend build
# ================================
FROM node:20-bookworm-slim AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

ENV NEXT_DISABLE_LIGHTNINGCSS=1
COPY frontend/ ./
RUN npm run build && npm prune --omit=dev


# ================================
# 🧱 Stage 3: Final runtime
# ================================
FROM python:3.11-slim AS runtime
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get install -y --no-install-recommends \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcairo2 libcups2 libdbus-1-3 \
    libdrm2 libgbm1 libglib2.0-0 libnss3 libnspr4 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxkbcommon0 \
    libpango-1.0-0 libpangocairo-1.0-0 fonts-liberation libfreetype6 \
    libfontconfig1 libxshmfence1 ca-certificates wget \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend-builder /app/backend/.venv ./backend/.venv
COPY --from=backend-builder /app/backend/src ./backend/src
COPY --from=backend-builder /app/backend/run_api.py ./backend/run_api.py

COPY --from=backend-builder /root/.cache/ms-playwright /root/.cache/ms-playwright

WORKDIR /app/frontend
COPY --from=frontend-builder /app/frontend/.next ./.next
COPY --from=frontend-builder /app/frontend/public ./public
COPY --from=frontend-builder /app/frontend/package.json .
COPY --from=frontend-builder /app/frontend/node_modules ./node_modules

WORKDIR /app
ENV PATH="/app/backend/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV NEXT_DISABLE_LIGHTNINGCSS=1

EXPOSE 8000 3000

RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'echo "--- Starting Backend API (Port 8000) ---"' >> /app/start.sh && \
    echo 'python /app/backend/run_api.py &' >> /app/start.sh && \
    echo 'echo "--- Starting Frontend Server (Port 3000) ---"' >> /app/start.sh && \
    echo 'cd /app/frontend && npm start' >> /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"]
