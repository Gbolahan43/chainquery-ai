from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Reusable Base
class UUIDModel(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# 1. NEW: The User Table
class User(UUIDModel, table=True):
    __tablename__ = "users"
    
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None, nullable=True)
    
    # Relationship: One User has Many Queries
    queries: List["UserQuery"] = Relationship(back_populates="user")

# 2. UPDATED: The Query Table
class UserQuery(UUIDModel, table=True):
    __tablename__ = "user_queries"

    user_input: str = Field(nullable=False)
    sql_output: Optional[str] = Field(default=None, nullable=True)  # Can be null if error occurs
    chain: str = Field(default="solana")
    
    # Auth Logic:
    # If Guest -> session_id is set, user_id is None
    # If Logged In -> user_id is set
    session_id: Optional[str] = Field(default=None, index=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    
    error_message: Optional[str] = Field(default=None)
    is_helpful: bool = Field(default=False)
    
    user: Optional[User] = Relationship(back_populates="queries")


