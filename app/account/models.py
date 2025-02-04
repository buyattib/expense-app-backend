import uuid
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

from .constants import AccountTypeEnum

if TYPE_CHECKING:
    from app.user.models import User
    from app.transaction.models import Transaction


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str]
    code: Mapped[str] = mapped_column(String(3))
    deleted: Mapped[bool] = mapped_column(default=False)

    # models relationships
    sub_accounts: Mapped[List["SubAccount"]] = relationship(back_populates="currency")


class AccountType(Base):
    __tablename__ = "account_types"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(50))
    code: Mapped[AccountTypeEnum]
    description: Mapped[Optional[str]]
    deleted: Mapped[bool] = mapped_column(default=False)

    accounts: Mapped[List["Account"]] = relationship(back_populates="account_type")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    deleted: Mapped[bool] = mapped_column(default=False)

    # foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    account_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("account_types.id"))

    # models relationships
    user: Mapped["User"] = relationship(back_populates="accounts")
    account_type: Mapped[List["AccountType"]] = relationship(back_populates="accounts")
    sub_accounts: Mapped[List["SubAccount"]] = relationship(back_populates="account")

    # unique account name and account type for each user
    __table_args__ = (
        UniqueConstraint(
            "name",
            "account_type_id",
            "user_id",
        ),
    )


# Table to be able to create one account with multiple currencies
class SubAccount(Base):
    __tablename__ = "sub_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    balance: Mapped[int] = mapped_column()  # saved in cents, ie, balance=100 is $1,00

    # foreign keys
    currency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("currencies.id"))
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.id"))

    # models relationships
    currency: Mapped["Currency"] = relationship(back_populates="sub_accounts")
    account: Mapped["Account"] = relationship(back_populates="sub_accounts")
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="sub_account"
    )

    # unique currency for a given account
    __table_args__ = (
        UniqueConstraint(
            "currency_id",
            "account_id",
        ),
        CheckConstraint(balance >= 0, name="balance_gte_0"),
    )
