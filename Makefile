.PHONY: dev build up down logs clean shell-backend

# --------------------------
# DEVELOPMENT (Local)
# --------------------------
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Uses 'concurrently' to run both without Docker for fast dev
dev-local:
	npx concurrently "cd backend && uvicorn app.main:app --reload" "cd frontend && npm run dev"

# --------------------------
# DOCKER PRODUCTION
# --------------------------
build:
	docker-compose -f docker-compose.prod.yml build

up:
	docker-compose -f docker-compose.prod.yml up -d

down:
	docker-compose -f docker-compose.prod.yml down

logs:
	docker-compose -f docker-compose.prod.yml logs -f

# --------------------------
# UTILITIES
# --------------------------
# Access the DB inside Docker
db-shell:
	docker exec -it chainquery_db psql -U postgres -d chainquery

# Run a migration inside the running backend container
migrate:
	docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
