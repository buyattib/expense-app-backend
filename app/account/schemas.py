from uuid import UUID
from typing import Annotated, Optional, List
from pydantic import BaseModel, ConfigDict, TypeAdapter, field_validator
from pydantic.types import StringConstraints
from .constants import AccountTypeEnum


### schemas -----------


# currency ---
class CurrencyBase(BaseModel):
    name: str
    code: Annotated[str, StringConstraints(max_length=3)]


class CurrencySchema(CurrencyBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


# account type ---
class AccountTypeBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    code: AccountTypeEnum
    description: Optional[str] = None


class AccountTypeSchema(AccountTypeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


# account ---
class AccountBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    description: Optional[str] = None

    account_type_id: str

    @field_validator("account_type_id", mode="before")
    @classmethod
    def account_type_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


class AccountSchema(AccountBase):
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


# sub account ---
class SubAccountBase(BaseModel):
    balance: int

    currency_id: str
    account_id: str

    @field_validator("currency_id", mode="before")
    @classmethod
    def currency_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v

    @field_validator("account_id", mode="before")
    @classmethod
    def account_id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


class SubAccountSchema(SubAccountBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v):
        return str(v) if isinstance(v, UUID) else v


### extended -----------


class SubAccountExtended(SubAccountSchema):
    currency: CurrencySchema

    model_config = ConfigDict(from_attributes=True)


class AccountExtended(AccountSchema):
    account_type: AccountTypeSchema
    sub_accounts: List[SubAccountExtended]

    model_config = ConfigDict(from_attributes=True)


### parameters ----------


class SubAccountParameter(BaseModel):
    currency_id: str
    balance: int


class CreateAccountParameters(AccountBase):
    sub_accounts: list[SubAccountParameter]


### pydantinc list adapters

CurrencySchemaListAdapter = TypeAdapter(List[CurrencySchema])
AccountTypeSchemaListAdapter = TypeAdapter(List[AccountTypeSchema])
AccountSchemaListAdapter = TypeAdapter(List[AccountSchema])
AccountExtendedListAdapter = TypeAdapter(List[AccountExtended])

"""
example:
CurrencySchemaListAdapter.validate_python([currency])
"""
