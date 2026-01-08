# app/models/enums.py
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    USER = "USER"
