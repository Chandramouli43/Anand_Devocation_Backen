# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from core.dependencies import get_current_user
from core.security import hash_password
from models.user import User
from models.enums import UserRole
from models.password_reset import PasswordResetOTP

from schemas.user import UserRead, UserUpdate, UserCreate
from schemas.password_reset import (
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
)

from core.otp import generate_otp, hash_otp, verify_otp, otp_expiry

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

# =====================================================
# CREATE – User self registration
# =====================================================

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        role=UserRole.USER,     # 🔒 forced
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# =====================================================
# READ – Get my profile
# =====================================================

@router.get("/me", response_model=UserRead)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user

# =====================================================
# UPDATE – Update my profile (SAFE FIELDS ONLY)
# =====================================================

@router.put("/me", response_model=UserRead)
def update_my_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user

# =====================================================
# DELETE – Deactivate my account (soft delete)
# =====================================================

@router.delete("/me")
def deactivate_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already deactivated",
        )

    current_user.is_active = False
    db.commit()

    return {"message": "Account deactivated successfully"}

# =====================================================
# FORGOT PASSWORD – SEND OTP
# =====================================================

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()

    # 🔒 Prevent user enumeration
    if not user:
        return {"message": "If the account exists, OTP has been sent"}

    otp = generate_otp()

    reset = PasswordResetOTP(
        user_id=str(user.id),
        otp_hash=hash_otp(otp),
        expires_at=otp_expiry(),
    )

    db.add(reset)
    db.commit()

    # TODO: Send via email / SMS
    print("DEBUG OTP:", otp)  # ❌ REMOVE IN PRODUCTION

    return {"message": "OTP sent successfully"}

# =====================================================
# VERIFY OTP
# =====================================================

@router.post("/verify-otp")
def verify_otp_code(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    otp_entry = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.user_id == str(user.id),
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.expires_at.desc())
        .first()
    )

    if (
        not otp_entry
        or otp_entry.expires_at < datetime.utcnow()
        or not verify_otp(data.otp, otp_entry.otp_hash)
    ):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"message": "OTP verified successfully"}

# =====================================================
# RESET PASSWORD
# =====================================================

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    otp_entry = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.user_id == str(user.id),
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.expires_at.desc())
        .first()
    )

    if (
        not otp_entry
        or otp_entry.expires_at < datetime.utcnow()
        or not verify_otp(data.otp, otp_entry.otp_hash)
    ):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.password_hash = hash_password(data.new_password)
    otp_entry.is_used = True

    db.commit()

    return {"message": "Password reset successful"}
