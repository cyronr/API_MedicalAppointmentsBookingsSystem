from pydantic import BaseModel
from uuid import UUID


class _UserBase(BaseModel):
    email: str


class User(_UserBase):
    id: int
    uuid: UUID


class UserCreate(_UserBase):
    password: str