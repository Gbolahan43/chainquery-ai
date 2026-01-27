from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.routes import router
from app.api.auth import router as auth_router
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (simplest for MVP)
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 1. CORS Configuration (CRITICAL for Frontend)
origins = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # Alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ... (Previous code remains)

# 2. Include Routes
app.include_router(router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

# Health Check for Railway/Render
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


# 3. Serve React Static Files (Modular Monolith)
# We check if the folder exists (it will in Docker, might not locally)
static_dir = os.path.join(os.getcwd(), "static_ui")

if os.path.exists(static_dir):
    # Mount assets (JS/CSS)
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    # Catch-All Route for SPA (Single Page Application)
    # This fixes the "Refresh on /dashboard gives 404" bug
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # If API is requested but not found above, return 404 (don't return HTML)
        if full_path.startswith("api"):
            return {"error": "API endpoint not found"}, 404
            
        # Otherwise, serve index.html
        return FileResponse(os.path.join(static_dir, "index.html"))

# Fallback for local dev (if static_ui doesn't exist)
@app.get("/")
async def root():
    return {"status": "ok", "message": "ChainQuery AI Backend Running (Local Mode)"}

