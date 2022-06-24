import datetime
from pydantic import BaseModel, validator
from uuid import UUID


class BookingCreate(BaseModel):
    patientId: UUID
    doctorId: UUID
    date: datetime.date
    time: datetime.time


class Booking(BookingCreate):
    id: UUID
    status: str
    no: str


class InternalBooking(BookingCreate):
    id: int = None
    statusId: int = None
    uuid: UUID = None
    internalPatientId: int = None
    internalDoctorId: int = None
