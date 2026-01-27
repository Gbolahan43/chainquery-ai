from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.config import settings
from app.core.security import ALGORITHM
from app.models.sql import User

# This tells FastAPI where to look for the token (Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    HYBRID AUTH:
    - If Token exists & is valid -> Return User object.
    - If Token is missing/invalid -> Return None (Treat as Guest).
    """
    if not token:
        return None

    try:
        # 1. Decode the Token
        payload = jwt.decode(token, settings.OPENAI_API_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None  # Invalid token, treat as guest

    # 2. Fetch User from DB
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user

async def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional)
) -> User:
    """
    STRICT AUTH:
    - Use this for routes that REQUIRE login (e.g., /profile, /settings).
    - If no user found, it raises 401 Error.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
