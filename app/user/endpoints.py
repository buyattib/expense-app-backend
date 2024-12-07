from fastapi import APIRouter

from app.auth.crud import CurrentUserDep
from . import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=schemas.UserSchema)
def read_users_me(
    current_user: CurrentUserDep,
):
    return current_user


# @router.get("/", response_model=list[schemas.UserSchema])
# def get_users(session: database.SessionDep):
#     return crud.get_users(session)


# @router.get("/{user_id}", response_model=schemas.UserSchema)
# def get_user(user_id: int, session: database.SessionDep):
#     db_user = crud.get_user(session, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     return db_user
