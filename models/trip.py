# app/models/trip.py

import enum
import uuid
from datetime import date

from sqlalchemy import String, Integer, Enum, Boolean, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class TripStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=False,
    )

    # ✅ Python type in annotation
    # ✅ SQLAlchemy type in mapped_column
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus),
        default=TripStatus.DRAFT,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
