# app/core/init_admin.py
from sqlalchemy.orm import Session
from models.user import User
from models.enums import UserRole
from core.security import hash_password
from core.config import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_NAME,
)

def create_default_admin(db: Session):
    admin = db.query(User).filter(User.email == DEFAULT_ADMIN_EMAIL).first()

    if admin:
        return  # ✅ already exists, do nothing

    admin = User(
        name=DEFAULT_ADMIN_NAME,
        email=DEFAULT_ADMIN_EMAIL,
        password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
        role=UserRole.ADMIN,
        is_active=True,
    )

    db.add(admin)
    db.commit()
    print("✅ Default admin created")
