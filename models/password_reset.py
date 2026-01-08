import uuid
from datetime import datetime, timedelta

from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    otp_hash: Mapped[str] = mapped_column(String, nullable=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
