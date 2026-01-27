from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# models.py
from pydantic import BaseModel

class LogoutRequest(BaseModel):
    refresh_token: str

# models.py
from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh_token: str
