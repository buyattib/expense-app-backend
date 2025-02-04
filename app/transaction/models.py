import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

from .constants import TransactionType

if TYPE_CHECKING:
    from app.user.models import User
    from app.account.models import SubAccount


# TODO:
# - new table with some common transaction categories to ask users if
#   they want to add selected ones so they dont have to do it manually.
# - in those categories include a "transfer between accounts one" as
#   intra account transfers will be just another category.
# - new model to tack transfers between accounts


class TransactionCategory(Base):
    __tablename__ = "transaction_categories"

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

    # models relationships
    user: Mapped["User"] = relationship(back_populates="transaction_categories")
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="transaction_category"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "name",
        ),
    )


# only for incomes and expenses
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    amount: Mapped[int] = mapped_column()  # saved in cents, ie, amount=100 is $1,00
    description: Mapped[Optional[str]]
    transaction_type: Mapped[TransactionType]
    deleted: Mapped[bool] = mapped_column(default=False)

    # foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    transaction_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("transaction_categories.id"), nullable=False
    )
    sub_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sub_accounts.id"), nullable=False
    )

    # models relationships
    user: Mapped["User"] = relationship(back_populates="transactions")
    transaction_category: Mapped["TransactionCategory"] = relationship(
        back_populates="transactions"
    )
    sub_account: Mapped["SubAccount"] = relationship(back_populates="transactions")

    __table_args__ = (CheckConstraint(amount > 0, name="amount_gt_0"),)
