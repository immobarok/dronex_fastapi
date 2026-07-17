from pydantic import EmailStr
from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class LoginData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email:EmailStr

class VerifyOTPRequest(BaseModel):
    email:EmailStr
    otp:str
class ResetPasswordRequest(BaseModel):
    token:str
    new_password:str
    
