from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas

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

    db_transaction_category = models.TransactionCategory(
        **transaction_category_data.model_dump(), user_id=user_id
    )
    session.add(db_transaction_category)
    session.commit()
    session.refresh(db_transaction_category)

    return db_transaction_category


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
    db_transaction = models.Transaction(
        **transaction_data.model_dump(), user_id=user_id
    )
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)

    return db_transaction


def get_transactions(session: Session, user_id: str):
    stmt = select(models.Transaction).where(
        models.Transaction.user_id == user_id, models.Transaction.deleted == False
    )
    result = session.scalars(stmt).all()

    return result


def get_transaction(session: Session, transaction_id: str):
    stmt = select(models.Transaction).where(models.Transaction.id == transaction_id)
    result = session.scalars(stmt).first()

    return result
