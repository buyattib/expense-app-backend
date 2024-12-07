from datetime import datetime
from typing import Annotated, Optional, List
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.types import StringConstraints, PositiveInt

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


# transactions ---
class TransactionBase(BaseModel):
    date: datetime
    amount: PositiveInt
    description: Optional[str] = None
    transaction_type: TransactionType
    transaction_category_id: str
    account_id: str


class TransactionSchema(TransactionBase):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)


### parameters and responses -----------


### pydantinc list adapters

TransactionCategorySchemaListAdapter = TypeAdapter(List[TransactionCategorySchema])
TransactionSchemaListAdapter = TypeAdapter(List[TransactionSchema])
