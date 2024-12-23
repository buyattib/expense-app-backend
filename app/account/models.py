from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.lib.utils import generate_uuid


if TYPE_CHECKING:
    from app.user.models import User
    from app.transaction.models import Transaction


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(String(3))
    deleted: Mapped[bool] = mapped_column(default=False)

    # models relationships
    accounts: Mapped[List["Account"]] = relationship(back_populates="currency")


class AccountType(Base):
    __tablename__ = "account_types"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    deleted: Mapped[bool] = mapped_column(default=False)

    accounts: Mapped[List["Account"]] = relationship(back_populates="account_type")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    balance: Mapped[int] = mapped_column()  # saved in cents, ie, balance=100 is $1,00
    deleted: Mapped[bool] = mapped_column(default=False)

    # foreign keys
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    currency_id: Mapped[str] = mapped_column(ForeignKey("currencies.id"))
    account_type_id: Mapped[str] = mapped_column(ForeignKey("account_types.id"))

    # models relationships
    user: Mapped["User"] = relationship(back_populates="accounts")
    currency: Mapped["Currency"] = relationship(back_populates="accounts")
    account_type: Mapped[List["AccountType"]] = relationship(back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account")

    # unique account name in a currency and of an account type
    __table_args__ = (
        UniqueConstraint(
            "name",
            "currency_id",
            "account_type_id",
            "user_id",
        ),
        CheckConstraint(balance >= 0, name="balance_gte_0"),
    )
