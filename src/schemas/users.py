from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from uuid import UUID


class PersonInfo(BaseModel):
    firstname: str
    surname: str
    phone: Optional[str]
    identificationNumber: Optional[str]
    identificationNumberType: Optional[int]
    city: Optional[str]
    street: Optional[str]
    zipCode: Optional[str]

    @validator('phone')
    def phone_must_be_numeric(cls, v):
        if not v:
            return v
        if not v.isnumeric():
            raise ValueError('Numer telefonu musi składać się z samych cyfr')
        return v


class _UserBase(BaseModel):
    email: EmailStr
    typeId: int = 10
    personInfo: PersonInfo = None


class User(_UserBase):
    id: UUID


class UserCreate(_UserBase):
    password: str
    password_confirm: str

    @validator('password_confirm')
    def passwords_must_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Hasła się nie zgadzają')
        return v


class InternalPersonInfo(PersonInfo):
    personId: int = None


class InternalUser(UserCreate, _UserBase):
    id: int = None
    statusId: int = None
    personId: int = None
    uuid: UUID = None
    password: str = None

