from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# INPUT: What the frontend sends
class QueryRequest(BaseModel):
    user_input: str
    chain: str = "solana"
    session_id: str  # <--- NEW: The Guest ID

# OUTPUT: What we send back
class QueryResponse(BaseModel):
    id: uuid.UUID
    user_input: str
    sql_output: str
    error: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

