import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from pwdlib import PasswordHash
from jose import jwt

load_dotenv()

# SECRET_KEY must be set via the SECRET_KEY environment variable in production.
# The fallback value below is only for local development convenience and must
# NEVER be used in a deployed environment.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-fallback-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
