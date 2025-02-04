from uuid import UUID
from typing import List
from sqlalchemy import select
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


def create_account(
    session: Session,
    user_id: UUID,
    account_data: schemas.AccountBase,
    sub_accounts_data: List[schemas.SubAccountParameter],
):
    same_account_stmt = select(models.Account).where(
        models.Account.user_id == user_id,
        models.Account.account_type_id == account_data.account_type_id,
        models.Account.name == account_data.name,
    )
    same_account = session.scalars(same_account_stmt).all()
    if len(same_account) > 1:
        raise Exception("There are repeated accounts")

    elif len(same_account) == 1:
        same_account = same_account[0]
        if not same_account.deleted:
            raise Exception("The account already exists")

        if same_account.deleted:
            same_account.deleted = False
            session.add(same_account)
            session.commit()
            session.refresh(same_account)
            return same_account

    db_account = models.Account(**account_data.model_dump(), user_id=user_id)
    session.add(db_account)

    currency_ids = [sub_acc.currency_id for sub_acc in sub_accounts_data]
    currencies = session.scalars(
        select(models.Currency).where(models.Currency.id._in(currency_ids))
    ).all()
    if len(currencies) != len(currency_ids):
        raise Exception("Some of the passed currencies are invalid")

    for sub_acc in sub_accounts_data:
        sub_account = models.SubAccount(
            account_id=db_account.id,
            currency_id=sub_acc.currency_id,
            balance=sub_acc.balance,
        )
        session.add(sub_account)

    session.commit()
    session.refresh(db_account)

    return db_account


def get_accounts(session: Session, user_id: UUID):
    stmt = (
        select(models.Account, models.AccountType)
        .join(models.AccountType)
        .where(
            models.Account.user_id == user_id,
            models.Account.deleted == False,
        )
    )
    # stmt = (
    #     select(models.Account, models.Currency, models.AccountType)
    #     .join(models.Currency)
    #     .join(models.AccountType)
    #     .where(
    #         models.Account.user_id == user_id,
    #         models.Account.deleted == False,
    #     )
    # )

    result = session.scalars(stmt).all()
    return result


def get_account(session: Session, account_id: str):
    stmt = select(models.Account).where(
        models.Account.id == account_id,
        models.Account.deleted == False,
    )
    result = session.scalars(stmt).first()
    return result
