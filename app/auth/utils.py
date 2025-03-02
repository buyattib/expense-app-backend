import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.config import settings

from app.user.schemas import UserSchema
from app.user.models import User
from .schemas import TokenPayload, TokenPayloadCreate, AuthenticationResponse


def decode_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.algorithm],
        )
        return TokenPayload(**payload)
    except jwt.PyJWTError as e:
        raise e


def generate_token(
    token_data: TokenPayloadCreate,
    expire_minutes: int,
    key: str,
):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode = TokenPayload(
        **token_data.model_dump(),
        exp=expiration,
        jti=str(uuid4()),
    )

    encoded_jwt = jwt.encode(
        to_encode.model_dump(),
        key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def generate_access_refresh_tokens(user: User):
    token_data = TokenPayloadCreate(
        sub=user.email,
        id=user.id,
    )

    access_token = generate_token(
        token_data=token_data,
        expire_minutes=settings.access_token_expire_minutes,
        key=settings.access_secret_key,
    )

    token_data.version = user.refresh_token_version
    refresh_token = generate_token(
        token_data=token_data,
        expire_minutes=settings.refresh_token_expire_minutes,
        key=settings.refresh_secret_key,
    )

    user_response = UserSchema.model_validate(user)

    return AuthenticationResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_expire_minutes,
        uid=user.id,
        info=user_response,
    )
