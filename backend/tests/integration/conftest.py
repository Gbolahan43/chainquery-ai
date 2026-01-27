"""
Pytest configuration for integration tests
"""
import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from unittest.mock import AsyncMock, MagicMock
import sys

# Mock the agent workflow before importing app
sys.modules['app.agent'] = MagicMock()
sys.modules['app.agent.workflow'] = MagicMock()

# Create a mock agent_app
mock_agent = AsyncMock()
mock_agent.ainvoke = AsyncMock(return_value={
    "sql_output": "SELECT * FROM solana.core.fact_transactions LIMIT 10;",
    "error": None
})
sys.modules['app.agent.workflow'].agent_app = mock_agent

from app.main import app
from app.core.database import get_db
from app.models.sql import UUIDModel

# Test database URL (use main database for now, will be cleaned after tests)
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/chainquery"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )
    
    yield engine
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database session"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
