from typing import Annotated, Optional, List
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.types import StringConstraints


### schemas -----------


# currency ---
class CurrencyBase(BaseModel):
    name: str
    code: Annotated[str, StringConstraints(max_length=3)]


class CurrencySchema(CurrencyBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


# account type ---
class AccountTypeBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    code: Annotated[str, StringConstraints(max_length=50)]
    description: Optional[str] = None


class AccountTypeSchema(AccountTypeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


# account ---
class AccountBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Optional[str] = None
    balance: int

    currency_id: str
    account_type_id: str


class AccountSchema(AccountBase):
    id: str

    user_id: str
    model_config = ConfigDict(from_attributes=True)


### parameters and responses -----------


class AccountExtended(AccountSchema):
    currency: CurrencySchema
    account_type: AccountTypeSchema

    model_config = ConfigDict(from_attributes=True)


### pydantinc list adapters

CurrencySchemaListAdapter = TypeAdapter(List[CurrencySchema])
AccountTypeSchemaListAdapter = TypeAdapter(List[AccountTypeSchema])
AccountSchemaListAdapter = TypeAdapter(List[AccountSchema])
AccountExtendedListAdapter = TypeAdapter(List[AccountExtended])


"""
example:
CurrencySchemaListAdapter.validate_python([currency])
"""
