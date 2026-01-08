from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from core.database import get_db
from models.user import User
from models.enums import UserRole
from core.security import oauth2_scheme
from core.config import SECRET_KEY, ALGORITHM


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    return user


def require_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


def require_agent(user: User = Depends(get_current_user)):
    if user.role != UserRole.AGENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent access required",
        )
    return user
