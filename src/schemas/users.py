from pydantic import BaseModel, validator, EmailStr
from uuid import UUID


class _UserBase(BaseModel):
    email: EmailStr

    # @validator('email')
    # def is_email_valid(cls, v):
    #     if '@' not in v:
    #         raise ValueError('Niepoprawny adres email')
    #     return v


class User(_UserBase):
    id: int
    uuid: UUID


class UserCreate(_UserBase):
    password: str


class UserInternal(UserCreate, _UserBase):
    status_id: int = None
    uuid: UUID = None
