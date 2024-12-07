from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.user.schemas import UserSchema

# token have registered claims (standards) and custom ones


class TokenPayloadCreate(BaseModel):
    id: str  # custom
    sub: str  # registered
    version: Optional[int] = None


class TokenPayload(TokenPayloadCreate):
    exp: datetime  # registered
    jti: str  # registered


class AuthenticationResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    uid: str
    info: UserSchema


class Refresh(BaseModel):
    refresh_token: str


class MagicLogin(BaseModel):
    email: EmailStr


class MagicLoginValidation(BaseModel):
    magic_token: str
