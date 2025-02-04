from uuid import UUID
from typing import List, Optional
from pydantic import ConfigDict, TypeAdapter, EmailStr, BaseModel, field_validator


### schemas -----------


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v) if isinstance(v, UUID) else v


### parameters and responses -----------


class UserCreate(BaseModel):
    email: EmailStr


### pydantinc list adapters

UserSchemaListAdapter = TypeAdapter(List[UserSchema])
