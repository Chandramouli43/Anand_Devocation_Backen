from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from core.database import Base


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )

    title: Mapped[str] = mapped_column(String(200))
    image_url: Mapped[str] = mapped_column(String(500))
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
