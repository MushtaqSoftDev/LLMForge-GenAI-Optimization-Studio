# Fly.io: Single image for frontend + backend (Postgres via Fly Postgres or Neon)
# Frontend served by nginx, proxies /api to backend

# --- Frontend build ---
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# --- Backend ---
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential nginx && \
    rm -rf /var/lib/apt/lists/*

# Backend deps (CPU-only torch for smaller image)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend /app/dist /var/www/html

# Nginx: serve static + proxy /api to localhost:8000
COPY deploy/nginx-fly.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 8080

COPY deploy/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
