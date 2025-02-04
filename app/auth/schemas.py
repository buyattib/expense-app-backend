from uuid import UUID
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, field_validator

from app.user.schemas import UserSchema

# token have registered claims (standards) and custom ones


class TokenPayloadCreate(BaseModel):
    id: Optional[Union[UUID, str]]  # custom
    sub: str  # registered
    version: Optional[int] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if isinstance(v, UUID) else v


class TokenPayload(TokenPayloadCreate):
    exp: datetime  # registered
    jti: str  # registered


class AuthenticationResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    uid: Union[UUID, str]
    info: UserSchema

    @field_validator("uid", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if isinstance(v, UUID) else v


class Refresh(BaseModel):
    refresh_token: str


class MagicLogin(BaseModel):
    email: EmailStr


class MagicLoginValidation(BaseModel):
    magic_token: str
