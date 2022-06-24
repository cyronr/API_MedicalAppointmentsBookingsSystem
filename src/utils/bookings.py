import logging
from sqlalchemy import text
from enum import Enum
from uuid import uuid4
from src.engine.db import IsolationLevel
from src.engine.logger import get_logger_name
from src.engine.errors import ParsingError, NotFound
import src.schemas.bookings as booking_schema
import src.sql.bookings as booking_sql

logger = logging.getLogger(f'{get_logger_name()}.utils.bookings')


class BookingStatus(int, Enum):
    PREPARED = 10
    CONFIRMED = 20
    CANCELLED = 30


class BookingEventType(int, Enum):
    CREATED = 10
    MODIFIED = 20
    CONFIRMED = 30
    CANCELLED = 40


def _parse_to_model(db_row):
    try:
        return booking_schema.Booking(
            id=db_row['UUID'],
            doctorId=db_row['DoctorPersonId'],
            patientId=db_row['PatientPersonId'],
            status=db_row['StatusName'],
            date=db_row['Date'],
            time=db_row['Time'],
            no=db_row['No']
        )
    except Exception as err:
        msg = f'Błąd parsowania rezerwacji: {err}'
        logger.critical(msg)
        raise ParsingError(msg)


def get_booking_by_id(db, booking_id):
    try:
        with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
            result = conn.execute(
                text(booking_sql.get_by_id),
                {'id': booking_id}
            )
            booking = result.fetchone()

            if not booking:
                raise Exception(f'Brak rezerwacji w bazie danych (booking_id: {booking_id})')

        return _parse_to_model(booking)
    except Exception as err:
        logger.error(err)
        raise


def get_booking_by_uuid(db, uuid):
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
        result = conn.execute(
            text(booking_sql.get_by_uuid),
            {'uuid': uuid}
        )
        booking = result.fetchone()

    return _parse_to_model(booking) if booking else None


def get_bookings_by_user(db, user_id):
    bookings = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(
            text(booking_sql.get_by_user_uuid),
            {'uuid': user_id}
        )
        for row in result:
            bookings.append(_parse_to_model(row))
    return bookings


def get_internal_person_id(db, uuid):
    try:
        with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
            result = conn.execute(
                text(booking_sql.get_internal_personId_by_uuid),
                {'uuid': uuid}
            )
            user = result.fetchone()

            if not user:
                raise NotFound(f'Nie znaleziono użytkownika o podanym indentyfikatorze. {uuid})')

        return user['PersonId']
    except Exception as err:
        logger.error(err)
        raise


def create_booking(db, booking: booking_schema.BookingCreate):
    internal_booking= booking_schema.InternalBooking(
        **booking.dict(),
        statusId=BookingStatus.PREPARED,
        uuid=uuid4(),
        internalDoctorId=get_internal_person_id(db, booking.doctorId),
        internalPatientId=get_internal_person_id(db, booking.patientId)
    )

    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        with conn.begin():
            internal_booking.id = conn.execute(
                text(booking_sql.create_booking),
                internal_booking.dict()
            ).scalar()

            conn.execute(
                text(booking_sql.create_booking_event),
                {
                    'booking_id': internal_booking.id,
                    'type_id': BookingEventType.CREATED
                }
            )

            return get_booking_by_id(db, internal_booking.id)


def confirm_booking(db, booking: booking_schema.Booking):
    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        result = conn.execute(
            text(booking_sql.get_by_uuid),
            {'uuid': booking.id}
        )
        db_booking = result.fetchone()
        internal_booking_id = db_booking['Id']

        with conn.begin():
            conn.execute(
                text(booking_sql.update_by_id),
                {
                    'id': internal_booking_id,
                    'status_id': BookingStatus.CONFIRMED
                }
            )

            conn.execute(
                text(booking_sql.create_booking_event),
                {
                    'booking_id': internal_booking_id,
                    'type_id': BookingEventType.CONFIRMED
                }
            )

            return get_booking_by_id(db, internal_booking_id)


def delete_booking(db, booking: booking_schema.Booking):
    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        result = conn.execute(
            text(booking_sql.get_by_uuid),
            {'uuid': booking.id}
        )
        db_booking = result.fetchone()
        internal_booking_id = db_booking['Id']

        with conn.begin():
            conn.execute(
                text(booking_sql.update_by_id),
                {
                    'id': internal_booking_id,
                    'status_id': BookingStatus.CANCELLED
                }
            )

            conn.execute(
                text(booking_sql.create_booking_event),
                {
                    'booking_id': internal_booking_id,
                    'type_id': BookingEventType.CANCELLED
                }
            )
    return {}

