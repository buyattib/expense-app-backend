from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas

# currency ----


def create_currency(session: Session, currency_data: schemas.CurrencyBase):
    db_currency = models.Currency(**currency_data.model_dump())

    session.add(db_currency)
    session.commit()
    session.refresh(db_currency)

    return db_currency


def get_currencies(session: Session):
    stmt = select(models.Currency).where(models.Currency.deleted == False)
    result = session.scalars(stmt).all()
    return result


# account type ----


def create_account_type(session: Session, account_type_data: schemas.AccountTypeBase):
    db_account_type = models.AccountType(**account_type_data.model_dump())

    session.add(db_account_type)
    session.commit()
    session.refresh(db_account_type)

    return db_account_type


def get_account_types(session: Session):
    stmt = select(models.AccountType).where(models.AccountType.deleted == False)
    result = session.scalars(stmt).all()
    return result


# account ----


def create_account(session: Session, user_id: str, account_data: schemas.AccountBase):
    accounts_q = select(func.count()).where(
        models.Account.user_id == user_id,
        models.Account.currency_id == account_data.currency_id,
        models.Account.account_type_id == account_data.account_type_id,
        models.Account.name == account_data.name,
        models.Account.deleted == False,
    )
    accounts_n = session.scalar(accounts_q)
    if accounts_n and accounts_n > 0:
        raise Exception("An account with the same parameters already exists")

    db_account = models.Account(**account_data.model_dump(), user_id=user_id)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    return db_account


def get_accounts(session: Session, user_id: str):
    stmt = (
        select(models.Account, models.Currency, models.AccountType)
        .join(models.Currency)
        .join(models.AccountType)
        .where(
            models.Account.user_id == user_id,
            models.Account.deleted == False,
        )
    )

    result = session.scalars(stmt).all()
    return result


def get_account(session: Session, account_id: str):
    stmt = (
        select(models.Account, models.Currency, models.AccountType)
        .where(
            models.Account.id == account_id,
            models.Account.deleted == False,
        )
        .join(models.Currency)
        .join(models.AccountType)
    )
    result = session.scalars(stmt).first()
    return result
