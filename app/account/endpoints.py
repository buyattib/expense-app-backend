from typing import List
from fastapi import APIRouter, HTTPException, status

from app.core import database
from app.auth import CurrentUserDep
from . import schemas, crud

# currency

currency_router = APIRouter(
    prefix="/currencies",
    tags=["Currencies"],
)


@currency_router.get("/", response_model=List[schemas.CurrencySchema])
def get_currencies(session: database.SessionDep, _: CurrentUserDep):
    currencies = crud.get_currencies(session)
    return currencies


# account type

account_type_router = APIRouter(
    prefix="/account-types",
    tags=["Account types"],
)


@account_type_router.get("/", response_model=List[schemas.AccountTypeSchema])
def get_account_types(session: database.SessionDep, _: CurrentUserDep):
    account_types = crud.get_account_types(session)
    return account_types


# account

account_router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@account_router.post("/", response_model=schemas.AccountSchema)
def create_account(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    account_data: schemas.CreateAccountParameters,
):
    try:
        return crud.create_account(
            session,
            current_user.id,
            account_data,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@account_router.get("/", response_model=List[schemas.AccountExtended])
def get_accounts(session: database.SessionDep, current_user: CurrentUserDep):
    accounts = crud.get_accounts(session, current_user.id)
    return accounts


@account_router.get("/{account_id}", response_model=schemas.AccountSchema)
def get_account(
    session: database.SessionDep,
    current_user: CurrentUserDep,
    account_id: str,
):
    account = crud.get_account(session, account_id=account_id)
    if account is None or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    return account


# populate constants tables


@currency_router.post(
    "/",
)
def create_currency(
    session: database.SessionDep,
):
    currencies_data = [
        schemas.CurrencyBase(name="Argentine Peso", code="ARS"),
        schemas.CurrencyBase(name="United States Dollar", code="USD"),
    ]

    for currency_data in currencies_data:
        db_c = crud.create_currency(session, currency_data)
        print(db_c.id)

    return {"status": "success"}


@account_type_router.post(
    "/",
)
def create_account_type(
    session: database.SessionDep,
):
    from .constants import AccountTypeEnum

    account_types_data = [
        schemas.AccountTypeBase(
            name=" ".join(at.value.split("_")).title(),
            code=at,
        )
        for at in AccountTypeEnum
    ]

    for account_type_data in account_types_data:
        db_at = crud.create_account_type(session, account_type_data)
        print(db_at.id)

    return {"status": "success"}
