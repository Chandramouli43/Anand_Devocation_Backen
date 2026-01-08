# app/models/location.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
import uuid

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
