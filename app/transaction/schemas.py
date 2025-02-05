from uuid import UUID
from datetime import datetime
from typing import Annotated, Optional, List
from pydantic import BaseModel, ConfigDict, TypeAdapter, field_validator
from pydantic.types import StringConstraints, PositiveInt

from app.account import schemas as account_schemas

from .constants import TransactionType


### schemas -----------


# transaction categories ---
class TransactionCategoryBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Optional[str] = None


class TransactionCategorySchema(TransactionCategoryBase):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v

    @field_validator("user_id", mode="before")
    @classmethod
    def user_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


# transactions ---
class TransactionBase(BaseModel):
    date: datetime
    amount: PositiveInt
    description: Optional[str] = None
    transaction_type: TransactionType
    transaction_category_id: str
    sub_account_id: str

    @field_validator("transaction_category_id", mode="before")
    @classmethod
    def transaction_category_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v

    @field_validator("sub_account_id", mode="before")
    @classmethod
    def account_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


class TransactionSchema(TransactionBase):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v

    @field_validator("user_id", mode="before")
    @classmethod
    def user_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


### extended -----------


class TransactionExtended(TransactionSchema):
    transaction_category: TransactionCategorySchema
    account: account_schemas.AccountSchema

    model_config = ConfigDict(from_attributes=True)


### parameters -----------


### pydantinc list adapters

TransactionCategorySchemaListAdapter = TypeAdapter(List[TransactionCategorySchema])
TransactionSchemaListAdapter = TypeAdapter(List[TransactionSchema])
TransactionExtendedListAdapter = TypeAdapter(List[TransactionExtended])
