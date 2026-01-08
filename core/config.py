# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# =======================
# Database
# =======================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")


# =======================
# Security / JWT
# =======================
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


# =======================
# Default Admin (Seeder)
# =======================
DEFAULT_ADMIN_EMAIL = os.getenv(
    "DEFAULT_ADMIN_EMAIL",
    "admin@ananddevocation.com",
)

DEFAULT_ADMIN_PASSWORD = os.getenv(
    "DEFAULT_ADMIN_PASSWORD",
    "Admin@123",
)

DEFAULT_ADMIN_NAME = os.getenv(
    "DEFAULT_ADMIN_NAME",
    "System Admin",
)

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")