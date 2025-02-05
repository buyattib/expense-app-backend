from uuid import UUID
from typing import Union
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.account import models as account_models, crud as account_crud

from . import models, schemas, constants

# transaction category ---


def create_transaction_category(
    session: Session,
    user_id: UUID,
    transaction_category_data: schemas.TransactionCategoryBase,
):
    existing_tx_categories = session.scalars(
        select(models.TransactionCategory).where(
            models.TransactionCategory.user_id == user_id,
            models.TransactionCategory.name == transaction_category_data.name,
        )
    ).all()
    if len(existing_tx_categories) > 1:
        raise Exception("There are repeated transaction categories")

    elif len(existing_tx_categories) == 1:
        existing_tx_categorie = existing_tx_categories[0]
        if not existing_tx_categorie.deleted:
            raise Exception("The transaction category already exists")
        else:
            existing_tx_categorie.deleted = False
            session.add(existing_tx_categorie)
            session.commit()
            session.refresh(existing_tx_categorie)
            return existing_tx_categorie

    transaction_category = models.TransactionCategory(
        **transaction_category_data.model_dump(), user_id=user_id
    )
    session.add(transaction_category)
    session.commit()
    session.refresh(transaction_category)

    return transaction_category


def get_transaction_categories(session: Session, user_id: UUID):
    stmt = select(models.TransactionCategory).where(
        models.TransactionCategory.user_id == user_id,
        models.TransactionCategory.deleted == False,
    )
    result = session.scalars(stmt).all()

    return result


def get_transaction_category(
    session: Session, transaction_category_id: Union[str, UUID]
):
    stmt = select(models.TransactionCategory).where(
        models.TransactionCategory.id == transaction_category_id,
        models.TransactionCategory.deleted == False,
    )
    result = session.scalars(stmt).first()

    return result


# transaction ---


def create_transaction(
    session: Session, user_id: UUID, transaction_data: schemas.TransactionBase
):

    sub_account = account_crud.get_sub_account(session, transaction_data.sub_account_id)
    if (
        not sub_account
        or sub_account.account.deleted
        or sub_account.account.user_id != user_id
    ):
        raise Exception("Account does not exist")

    transaction_category = get_transaction_category(
        session, transaction_data.transaction_category_id
    )
    if (
        not transaction_category
        or transaction_category.deleted
        or transaction_category.user_id != user_id
    ):
        raise Exception("Category does not exist")

    transaction = models.Transaction(**transaction_data.model_dump(), user_id=user_id)

    if transaction.transaction_type == constants.TransactionType.EXPENSE:
        if sub_account.balance - transaction.amount < 0:
            raise Exception("Insufficient balance in account")

        sub_account.balance -= transaction.amount
    elif transaction.transaction_type == constants.TransactionType.INCOME:
        sub_account.balance += transaction.amount

    session.add(transaction)
    session.add(sub_account)

    session.commit()

    session.refresh(transaction)
    session.refresh(sub_account)

    return transaction


def get_transactions(session: Session, user_id: UUID):
    stmt = (
        select(
            models.Transaction,
            models.TransactionCategory,
            account_models.SubAccount,
        )
        .join(models.TransactionCategory)
        .join(account_models.SubAccount)
        .where(
            models.Transaction.user_id == user_id,
            models.Transaction.deleted == False,
        )
        .order_by(models.Transaction.date.desc())
    )

    result = session.scalars(stmt).all()
    return result


def get_transaction(session: Session, transaction_id: Union[UUID, str]):
    stmt = select(
        models.Transaction,
    ).where(
        models.Transaction.id == transaction_id, models.Transaction.deleted == False
    )

    result = session.scalars(stmt).first()
    return result
