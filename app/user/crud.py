from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User


def get_user(session: Session, user_id: str):
    stmt = select(User).where(
        User.id == user_id,
        # User.deleted == False
    )
    result = session.scalar(stmt, {"id": user_id})

    return result


def get_users(session: Session):
    stmt = select(User)  # .where(User.deleted == False)
    result = session.scalars(stmt).all()

    return result


def get_user_by_email(session: Session, email: str):
    stmt = select(User).where(
        User.email == email,
        # User.deleted == False
    )
    result = session.scalar(stmt)

    return result


def create_user(
    session: Session,
    email: str,
):
    db_user = User(email=email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
