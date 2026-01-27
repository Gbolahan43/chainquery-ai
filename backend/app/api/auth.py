from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.sql import User
from app.core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

# Schema for Signup
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", response_model=Token)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if email exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 2. Create User
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # 3. Generate Token immediately (Auto-login)
    access_token = create_access_token(subject=new_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # OAuth2PasswordRequestForm expects 'username' and 'password' fields
    # We treat 'username' as 'email'
    
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
