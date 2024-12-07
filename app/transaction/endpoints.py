from typing import List
from fastapi import APIRouter, HTTPException, status

from app.core import database
from app.auth import CurrentUserDep
from . import schemas, crud


# transaction category ---

transaction_category_router = APIRouter(
    prefix="/transaction-categories",
    tags=["Transaction categories"],
)


@transaction_category_router.post("/", response_model=schemas.TransactionCategorySchema)
def create_transaction_category(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    transaction_category_data: schemas.TransactionCategoryBase,
):
    return crud.create_transaction_category(
        session, current_user.id, transaction_category_data
    )


@transaction_category_router.get(
    "/", response_model=List[schemas.TransactionCategorySchema]
)
def get_transaction_categories(
    session: database.SessionDep, current_user: CurrentUserDep
):
    return crud.get_transaction_categories(session, current_user.id)


@transaction_category_router.get(
    "/{transaction_category_id}", response_model=schemas.TransactionCategorySchema
)
def get_transaction_category(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    transaction_category_id: str,
):
    transaction_category = crud.get_transaction_category(
        session, transaction_category_id=transaction_category_id
    )
    if transaction_category is None or transaction_category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return transaction_category


# @transaction_category_router.post(
#     "/common", response_model=List[schemas.TransactionCategorySchema]
# )
# def create_common_transaction_category(
#     session: database.SessionDep,
#     current_user: CurrentUserDep,
#     # transaction_category_data: schemas.TransactionCategoryBase,
# ):
#     common_list = [
#         schemas.TransactionCategoryBase(name="Supermarket"),
#         schemas.TransactionCategoryBase(name="Restaurant"),
#         schemas.TransactionCategoryBase(name="Transportation"),
#         schemas.TransactionCategoryBase(name="Savings"),
#     ]
#
#     for tc in common_list:
#         return crud.create_transaction_category(session, current_user.id, tc)


# transaction ---

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@transaction_router.post("/", response_model=schemas.TransactionSchema)
def create_transaction(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    transaction_data: schemas.TransactionBase,
):
    return crud.create_transaction(session, current_user.id, transaction_data)


@transaction_router.get("/", response_model=list[schemas.TransactionSchema])
def get_transactions(session: database.SessionDep, current_user: CurrentUserDep):
    return crud.get_transactions(session, current_user.id)


@transaction_router.get("/{transaction_id}", response_model=schemas.TransactionSchema)
def get_transaction(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    transaction_id: str,
):
    transaction = crud.get_transaction(session, transaction_id=transaction_id)
    if transaction is None or transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    return transaction
