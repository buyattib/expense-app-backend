from typing import List, Optional
from pydantic import ConfigDict, TypeAdapter, EmailStr, BaseModel


### schemas -----------


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


### parameters and responses -----------


class UserCreate(BaseModel):
    email: EmailStr


### pydantinc list adapters

UserSchemaListAdapter = TypeAdapter(List[UserSchema])
