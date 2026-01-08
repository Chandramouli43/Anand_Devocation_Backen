# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Email + Password login.
    OAuth2 expects `username` field (we treat it as email).
    Works for Admin, Agent, User.
    """

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        subject=str(user.id),
        role=user.role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
