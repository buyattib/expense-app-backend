from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.config import settings
from app.core.database import SessionDep
from app.user import crud as user_crud, models as user_models

from . import utils


def get_current_user(
    session: Session, token: str, secret_key: str, is_refresh: bool = False
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = utils.decode_token(token, secret_key)
    except InvalidTokenError:
        raise credentials_exception

    if is_refresh and not payload.version:
        raise credentials_exception

    email = payload.sub
    if email is None or not payload.id:
        raise credentials_exception

    user = user_crud.get_user_by_email(session, email=email)
    if not user:
        raise credentials_exception

    if is_refresh and (payload.version != user.refresh_token_version):
        raise credentials_exception

    return user


def validate_new_user(session: Session, token: str, secret_key: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = utils.decode_token(token, secret_key)
    except InvalidTokenError:
        raise credentials_exception

    email = payload.sub
    if email is None or payload.id != "0":
        raise credentials_exception

    user = user_crud.get_user_by_email(session, email=email)
    if user:
        raise credentials_exception

    return email


# To use in endpoints whenever an access token is expected in the authorization header

# tokenUrl refers to the endpoint to get the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user_dep(session: SessionDep, token: TokenDep):
    return get_current_user(session, token, secret_key=settings.access_secret_key)


CurrentUserDep = Annotated[user_models.User, Depends(get_current_user_dep)]
