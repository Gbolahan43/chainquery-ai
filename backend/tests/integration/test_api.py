"""
Integration tests for ChainQuery AI API endpoints
Tests authentication, query generation, and history with database
"""
import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.main import app
from app.models.sql import User, UserQuery
from app.core.database import get_db


class TestAuthEndpoints:
    """Test authentication endpoints (signup, login)"""
    
    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient):
        """Test successful user signup"""
        email = f"test_{uuid.uuid4()}@example.com"
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": email,
                "password": "password123",
                "full_name": "Test User"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient):
        """Test signup with duplicate email fails"""
        email = f"duplicate_{uuid.uuid4()}@example.com"
        
        # First signup
        await client.post(
            "/api/v1/auth/signup",
            json={
                "email": email,
                "password": "password123",
                "full_name": "Test User"
            }
        )
        
        # Second signup with same email
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": email,
                "password": "password123",
                "full_name": "Test User 2"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient):
        """Test successful login"""
        email = f"login_{uuid.uuid4()}@example.com"
        password = "password123"
        
        # Signup first
        await client.post(
            "/api/v1/auth/signup",
            json={"email": email, "password": password, "full_name": "Test"}
        )
        
        # Login
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials fails"""
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent@example.com", "password": "wrong"}
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()


class TestGuestQueryGeneration:
    """Test guest user query generation and history"""
    
    @pytest.mark.asyncio
    async def test_guest_generate_query(self, client: AsyncClient):
        """Test guest can generate query with session_id"""
        session_id = str(uuid.uuid4())
        
        response = await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Show me top 10 SOL holders",
                "chain": "solana",
                "session_id": session_id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "sql_output" in data
        assert "user_input" in data
        assert data["user_input"] == "Show me top 10 SOL holders"
    
    @pytest.mark.asyncio
    async def test_guest_history_isolation(self, client: AsyncClient):
        """Test guest history is isolated by session_id"""
        session_1 = str(uuid.uuid4())
        session_2 = str(uuid.uuid4())
        
        # Guest 1 generates query
        await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Query from guest 1",
                "chain": "solana",
                "session_id": session_1
            }
        )
        
        # Guest 2 generates query
        await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Query from guest 2",
                "chain": "solana",
                "session_id": session_2
            }
        )
        
        # Get history for session_1
        response_1 = await client.get(
            f"/api/v1/history?session_id={session_1}"
        )
        
        # Get history for session_2
        response_2 = await client.get(
            f"/api/v1/history?session_id={session_2}"
        )
        
        assert response_1.status_code == 200
        assert response_2.status_code == 200
        
        data_1 = response_1.json()
        data_2 = response_2.json()
        
        # Each should have their own query
        assert len(data_1) >= 1
        assert len(data_2) >= 1
        
        # Verify isolation
        assert data_1[0]["user_input"] == "Query from guest 1"
        assert data_2[0]["user_input"] == "Query from guest 2"


class TestAuthenticatedQueryGeneration:
    """Test authenticated user query generation"""
    
    @pytest.mark.asyncio
    async def test_authenticated_generate_links_user(self, client: AsyncClient, db_session: AsyncSession):
        """Test authenticated query links to user_id"""
        email = f"auth_{uuid.uuid4()}@example.com"
        password = "password123"
        
        # Signup
        signup_response = await client.post(
            "/api/v1/auth/signup",
            json={"email": email, "password": password, "full_name": "Test"}
        )
        token = signup_response.json()["access_token"]
        
        # Generate query with auth
        response = await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Authenticated query",
                "chain": "solana",
                "session_id": str(uuid.uuid4())
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        
        # Verify user_id is set in database
        result = await db_session.execute(
            select(UserQuery).where(UserQuery.user_input == "Authenticated query")
        )
        query = result.scalars().first()
        
        assert query is not None
        assert query.user_id is not None


class TestHybridAuthentication:
    """Test hybrid guest/authenticated user scenarios"""
    
    @pytest.mark.asyncio
    async def test_guest_then_signup(self, client: AsyncClient):
        """Test guest can signup and continue"""
        session_id = str(uuid.uuid4())
        
        # Generate as guest
        await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Guest query",
                "chain": "solana",
                "session_id": session_id
            }
        )
        
        # Signup
        email = f"upgrade_{uuid.uuid4()}@example.com"
        signup_response = await client.post(
            "/api/v1/auth/signup",
            json={"email": email, "password": "password123", "full_name": "Test"}
        )
        token = signup_response.json()["access_token"]
        
        # Generate as authenticated user
        response = await client.post(
            "/api/v1/generate",
            json={
                "user_input": "Authenticated query after upgrade",
                "chain": "solana",
                "session_id": session_id
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
