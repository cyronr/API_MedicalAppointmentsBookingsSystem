import datetime
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class Specialty(BaseModel):
    id: int
    name: str
    main: bool


class Doctor(BaseModel):
    id: UUID
    firstname: str
    surname: str
    city: str
    street: str
    zipCode: str
    title: str
    specialties: Optional[List[Specialty]]


class Schedule(BaseModel):
    date: datetime.date
    time: datetime.time
    datetime: datetime.datetime
