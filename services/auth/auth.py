from jose import jwt
from datetime import datetime, timedelta
import uuid
import os

JWT_ALGO = "RS256"
ACCESS_EXPIRE_MIN = 15
REFRESH_EXPIRE_DAYS = 7

with open("private.pem") as f:
    PRIVATE_KEY = f.read()

with open("public.pem") as f:
    PUBLIC_KEY = f.read()

def create_access_token(user_id: str):
    payload = {
        "sub": user_id,
        "scope": "user",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MIN),
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=JWT_ALGO)

def create_refresh_token():
    return str(uuid.uuid4())
