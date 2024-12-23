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
    account_data: schemas.AccountBase,
):
    try:
        return crud.create_account(session, current_user.id, account_data)
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


# populate constats tables


@currency_router.post(
    "/",
    # response_model=schemas.CurrencyResponse
)
def create_currency(
    session: database.SessionDep,
    # currency_data: schemas.CurrencyBase,
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
    # response_model=schemas.AccountTypeResponse
)
def create_account_type(
    session: database.SessionDep,
    # account_type_data: schemas.AccountTypeBase,
):
    account_types_data = [
        schemas.AccountTypeBase(name="Cash", code="cash"),
        schemas.AccountTypeBase(name="Bank", code="bank"),
        schemas.AccountTypeBase(name="Digital Wallet", code="digital_wallet"),
        schemas.AccountTypeBase(name="Crypto Wallet", code="crypto_wallet"),
    ]

    for account_type_data in account_types_data:
        db_at = crud.create_account_type(session, account_type_data)
        print(db_at.id)

    return {"status": "success"}
