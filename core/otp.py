import random
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def hash_otp(otp: str) -> str:
    return pwd_context.hash(otp)


def verify_otp(otp: str, hashed: str) -> bool:
    return pwd_context.verify(otp, hashed)


def otp_expiry(minutes: int = 5):
    return datetime.utcnow() + timedelta(minutes=minutes)
