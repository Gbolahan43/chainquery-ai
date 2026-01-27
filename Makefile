# ChainQuery AI Makefile
# Windows-compatible (Powershell/CMD friendly where possible, but optimized for Git Bash/WSL usually)

.PHONY: install dev build test docker-up docker-down clean help

# Default target
help:
	@echo "ChainQuery AI Management Commands:"
	@echo "  make install      - Install backend and frontend dependencies"
	@echo "  make dev          - Run both backend and frontend locally"
	@echo "  make build        - Build the frontend for production"
	@echo "  make test         - Run backend tests"
	@echo "  make docker-up    - Start services with Docker Compose"
	@echo "  make docker-down  - Stop Docker Compose services"
	@echo "  make clean        - Remove temporary files"

# Install all dependencies
install:
	@echo "Installing Backend Dependencies..."
	cd backend && python -m venv venv && ./venv/Scripts/pip install -r requirements.txt
	@echo "Installing Frontend Dependencies..."
	cd frontend && npm install
	@echo "Installing Root Scripts..."
	npm install

# Run development servers concurrently
dev:
	npm run dev

# Build frontend
build:
	cd frontend && npm run build

# Run tests
test:
	cd backend && ./venv/Scripts/pytest

# Docker Management
docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

# Cleanup
clean:
	rm -rf backend/__pycache__
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf node_modules
