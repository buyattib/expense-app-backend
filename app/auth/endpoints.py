from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.config import settings

from app.core import database, logging
from app.user import crud as user_crud, schemas as user_schemas
from app.emails import fast_mail, create_email_html_message

from . import schemas, crud, utils


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/email-link")
async def email_link(
    session: database.SessionDep,
    body: schemas.MagicLogin,
    background_tasks: BackgroundTasks,
):

    # TODO: build a rate limiter to use with email and ip

    user = user_crud.get_user_by_email(session, email=body.email)

    token_data = schemas.TokenPayloadCreate(
        sub=body.email,
        id=user.id if user else "0",
    )
    magic_token = utils.generate_token(
        token_data=token_data,
        expire_minutes=settings.magic_token_expire_minutes,
        key=settings.magic_secret_key,
    )

    url = "login" if user else "signup"
    subject = "Login" if user else "Register"

    message = create_email_html_message(
        subject=subject,
        recipients=[body.email],
        template_body={
            "existing_user": bool(user),
            "login_url": f"{settings.frontend_host}/confirm/{url}?token={magic_token}",
        },
    )

    # send email task
    background_tasks.add_task(
        fast_mail.send_message, message, template_name="login.html"
    )

    return {"message": "An email was sent"}


@router.post(
    "/login",
    response_model=schemas.AuthenticationResponse,
)
async def login(
    session: database.SessionDep,
    body: schemas.MagicLoginValidation,
):
    user = crud.get_current_user(
        session=session,
        token=body.magic_token,
        secret_key=settings.magic_secret_key,
    )

    response = utils.generate_access_refresh_tokens(user)
    return response


@router.post(
    "/signup",
    response_model=schemas.AuthenticationResponse,
)
async def signup(
    session: database.SessionDep,
    body: schemas.MagicLoginValidation,
):
    email = crud.validate_new_user(
        session=session,
        token=body.magic_token,
        secret_key=settings.magic_secret_key,
    )

    try:
        user_create = user_schemas.UserCreate(email=email)
        user = user_crud.create_user(session=session, email=user_create.email)
        response = utils.generate_access_refresh_tokens(user)
        return response
    except Exception as e:
        logging.logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There was a problem with registration",
        )


@router.post(
    "/refresh",
    response_model=schemas.AuthenticationResponse,
)
def refresh(
    session: database.SessionDep,
    body: schemas.Refresh,
):
    user = crud.get_current_user(
        session=session,
        token=body.refresh_token,
        secret_key=settings.refresh_secret_key,
        is_refresh=True,
    )

    response = utils.generate_access_refresh_tokens(user)
    return response


# TODO: when logging out of all devices: increment refresh_token_version in user table
