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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include Routes
app.include_router(router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

# 3. Root Endpoint (Health Check)
@app.get("/")
async def root():
    return {"status": "ok", "message": "ChainQuery AI Backend is Running"}

