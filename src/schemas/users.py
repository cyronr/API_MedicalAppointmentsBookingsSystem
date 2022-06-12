from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from uuid import UUID


class PersonInfo(BaseModel):
    firstname: str
    surname: str
    phone: str
    identificationNumber: Optional[str]
    identificationNumberType: Optional[int] = 10
    city: Optional[str]
    street: Optional[str]
    zipCode: Optional[str]

    @validator('phone')
    def phone_must_be_numeric(cls, v):
        if not v.isnumeric():
            raise ValueError('Numer telefonu musi składać się z samych cyfr')
        return v

    @validator('identificationNumberType')
    def id_number_has_to_have_type(cls, v, values, **kwargs):
        if 'identificationNumber' in values and v is None:
            raise ValueError('Nieokreślony typ identyfikatora')
        return v


class _UserBase(BaseModel):
    email: EmailStr
    typeId: int = 10
    personInfo: PersonInfo = None


class User(_UserBase):
    id: UUID


class UserCreate(_UserBase):
    password: str


class InternalPersonInfo(PersonInfo):
    personId: int = None


class InternalUser(UserCreate, _UserBase):
    id: int = None
    statusId: int = None
    personId: int = None
    uuid: UUID = None
    password: str = None

