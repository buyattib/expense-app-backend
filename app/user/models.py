from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.lib.utils import generate_uuid

from app.transaction.models import TransactionCategory, Transaction
from app.account.models import Account


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    deleted: Mapped[bool] = mapped_column(default=False)

    refresh_token_version: Mapped[int] = mapped_column(default=1)

    # models relationships
    accounts: Mapped[List["Account"]] = relationship(back_populates="user")
    transaction_categories: Mapped[List["TransactionCategory"]] = relationship(
        back_populates="user"
    )
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
