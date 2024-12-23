from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.account import models as account_models, crud as account_crud

from . import models, schemas, constants

# transaction category ---


def create_transaction_category(
    session: Session,
    user_id: str,
    transaction_category_data: schemas.TransactionCategoryBase,
):
    existing_tx_categories_count = session.scalar(
        select(func.count()).where(
            models.TransactionCategory.user_id == user_id,
            models.TransactionCategory.name == transaction_category_data.name,
            models.TransactionCategory.deleted == False,
        )
    )
    if existing_tx_categories_count and existing_tx_categories_count > 0:
        raise Exception("A transaction category already exists with the same name")

    transaction_category = models.TransactionCategory(
        **transaction_category_data.model_dump(), user_id=user_id
    )
    session.add(transaction_category)
    session.commit()
    session.refresh(transaction_category)

    return transaction_category


def get_transaction_categories(session: Session, user_id: str):
    stmt = select(models.TransactionCategory).where(
        models.TransactionCategory.user_id == user_id,
        models.TransactionCategory.deleted == False,
    )
    result = session.scalars(stmt).all()

    return result


def get_transaction_category(session: Session, transaction_category_id: str):
    stmt = select(models.TransactionCategory).where(
        models.TransactionCategory.id == transaction_category_id,
        models.TransactionCategory.deleted == False,
    )
    result = session.scalars(stmt).first()

    return result


# transaction ---


def create_transaction(
    session: Session, user_id: str, transaction_data: schemas.TransactionBase
):
    transaction = models.Transaction(**transaction_data.model_dump(), user_id=user_id)
    transaction_category = get_transaction_category(
        session, transaction.transaction_category_id
    )
    account = account_crud.get_account(session, transaction.account_id)

    if not transaction_category or transaction_category.user_id != user_id:
        raise Exception("The selected category does not exist")

    if not account or account.user_id != user_id:
        raise Exception("The selected account does not exist")

    if transaction.transaction_type == constants.TransactionType.EXPENSE:
        account.balance -= transaction.amount
    elif transaction.transaction_type == constants.TransactionType.INCOME:
        account.balance += transaction.amount

    session.add(transaction)
    session.add(account)

    session.commit()

    session.refresh(transaction)
    session.refresh(account)

    return transaction


def get_transactions(session: Session, user_id: str):
    stmt = (
        select(
            models.Transaction,
            models.TransactionCategory,
            account_models.Account,
        )
        .join(models.TransactionCategory)
        .join(account_models.Account)
        .where(
            models.Transaction.user_id == user_id,
            models.Transaction.deleted == False,
        )
        .order_by(models.Transaction.date.desc())
    )

    result = session.scalars(stmt).all()
    return result


def get_transaction(session: Session, transaction_id: str):
    stmt = select(
        models.Transaction,
    ).where(
        models.Transaction.id == transaction_id, models.Transaction.deleted == False
    )

    result = session.scalars(stmt).first()
    return result
