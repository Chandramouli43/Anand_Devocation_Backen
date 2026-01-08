from datetime import date
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class TripStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
