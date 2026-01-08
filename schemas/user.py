from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    USER = "USER"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None


class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
