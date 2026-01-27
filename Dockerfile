# ---------------------------------------
# Stage 1: Build Frontend (Node.js)
# ---------------------------------------
FROM node:18-alpine AS frontend-builder
ENV FORCE_REBUILD=1

WORKDIR /frontend-build

# Copy frontend dependency files
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy source code and build
COPY frontend/ .
RUN ls -R /frontend-build/src
RUN npm run build
# Result: The static site is now in /frontend-build/dist

# ---------------------------------------
# Stage 2: Final Image (Python + Static Files)
# ---------------------------------------
FROM python:3.11-slim

WORKDIR /app

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy Backend Code
COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

# 4. Copy Built Frontend from Stage 1
# We put it in a specific folder to serve later
COPY --from=frontend-builder /frontend-build/dist ./static_ui

# 5. Environment Config
ENV PYTHONPATH=/app
ENV PORT=10000

# 6. Run Command
# We run migration + start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
