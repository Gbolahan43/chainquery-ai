from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.agent.workflow import agent_app
from app.models.sql import UserQuery, User
from app.schemas.requests import QueryRequest, QueryResponse
from app.api.deps import get_current_user_optional

router = APIRouter()

@router.post("/generate", response_model=QueryResponse)
async def generate_query(
    request: QueryRequest, 
    db: AsyncSession = Depends(get_db),
    # Inject the user (if logged in) or None (if guest)
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    HYBRID ENDPOINT:
    1. Receives natural language from user.
    2. Runs the LangGraph Agent.
    3. Saves the result with session_id (always) and user_id (if authenticated).
    4. Returns the SQL.
    """
    # 1. Run the Agent (only pass fields in AgentState)
    inputs = {"user_input": request.user_input}
    result = await agent_app.ainvoke(inputs)
    
    sql_result = result.get("sql_output")
    error_msg = result.get("error")

    # Debug logging
    print(f"Agent Result: sql_output={sql_result[:100] if sql_result else None}, error={error_msg}")

    # 2. Save to DB (Hybrid Logic)
    db_query = UserQuery(
        user_input=request.user_input,
        sql_output=sql_result or "",
        error_message=error_msg,
        chain=request.chain,
        session_id=request.session_id,  # Always save session_id (for device history)
        
        # LINK USER IF LOGGED IN
        user_id=current_user.id if current_user else None
    )
    
    db.add(db_query)
    await db.commit()
    await db.refresh(db_query)

    return db_query

@router.get("/history", response_model=list[QueryResponse])
async def get_history(
    session_id: str,  # <--- Require session_id as a query param
    limit: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch history for a specific Guest Session.
    Usage: GET /api/v1/history?session_id=123-abc
    """
    statement = (
        select(UserQuery)
        .where(UserQuery.session_id == session_id)  # <--- Filter by ID
        .order_by(UserQuery.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(statement)
    return result.scalars().all()

