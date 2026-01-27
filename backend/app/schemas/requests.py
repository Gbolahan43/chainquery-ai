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
    sql_output: Optional[str] = None  # Can be None if generation fails
    error_message: Optional[str] = None  # Match database field name
    chain: str = "solana"
    created_at: datetime
    
    class Config:
        from_attributes = True

