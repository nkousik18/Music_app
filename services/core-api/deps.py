from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import os

security = HTTPBearer()

with open("../auth/public.pem") as f:
    PUBLIC_KEY = f.read()

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(
            token.credentials,
            PUBLIC_KEY,
            algorithms=["RS256"]
        )
        return payload["sub"]
    except Exception:
        raise HTTPException(401, "Invalid token")
