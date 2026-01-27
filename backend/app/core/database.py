from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.core.config import settings
from app.models.sql import UUIDModel

# 1. Create Async Engine
# echo=True logs SQL queries to console (Good for debugging, turn off in Prod)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "dev"),
    future=True,
    pool_pre_ping=True  # Handles lost connections automatically
)

# 2. Session Factory
# This creates new sessions for each request
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def init_db():
    """Initialize database - create all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(UUIDModel.metadata.create_all)


# 3. Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency.
    Opens a session, yields it to the route, and closes it after response.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
