import logging
from sqlalchemy import text
from src.engine.db import IsolationLevel
from src.engine.logger import get_logger_name
from src.engine.errors import ParsingError
import src.schemas.doctors as doctor_schema
import src.sql.doctors as doctor_sql


logger = logging.getLogger(f'{get_logger_name()}.utils.doctors')


def _doctor_parse_to_model(db_row, specialties):
    try:
        return doctor_schema.Doctor(
            id=db_row['UUID'],
            firstname=db_row['Firstname'],
            surname=db_row['Surname'],
            city=db_row['City'],
            street=db_row['Street'],
            zipCode=db_row['ZipCode'],
            title=db_row['Title'],
            specialties=specialties
        )
    except Exception as err:
        msg = f'Błąd parsowania lekarza: {err}'
        logger.critical(msg)
        raise ParsingError(msg)


def _specialty_parse_to_model(db_row):
    try:
        return doctor_schema.Specialty(
            id=db_row['Id'],
            name=db_row['Name'],
            main=db_row['Main']
        )
    except Exception as err:
        msg = f'Błąd parsowania specializacji: {err}'
        logger.critical(msg)
        raise ParsingError(msg)


def _schedule_parse_to_model(db_row):
    try:
        return doctor_schema.Schedule(
            time=db_row['Time'],
            date=db_row['Date'],
            datetime=db_row['DateTime']
        )
    except Exception as err:
        msg = f'Błąd parsowania grafiku: {err}'
        logger.critical(msg)
        raise ParsingError(msg)


def get_doctor_specialties(db, doctor_id):
    specialties = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(
            text(doctor_sql.get_doctor_specialities),
            {'id': doctor_id}
        )
        for row in result:
            specialties.append(_specialty_parse_to_model(row))
    return specialties


def get_all_doctors(db):
    doctors = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(text(doctor_sql.get_all))
        for row in result:
            specialties = get_doctor_specialties(db, row['Id'])
            doctors.append(_doctor_parse_to_model(row, specialties))
    return doctors


def get_doctor_by_uuid(db, uuid):
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
        result = conn.execute(
            text(doctor_sql.get_by_uuid),
            {'uuid': uuid}
        )
        doctor = result.fetchone()
    specialties = get_doctor_specialties(db, doctor['Id'])
    return _doctor_parse_to_model(doctor, specialties) if doctor else None


def get_doctor_schedule(db, doctor: doctor_schema.Doctor):
    schedule = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(
            text(doctor_sql.get_doctor_schedule),
            {'uuid': doctor.id}
        )
        for row in result:
            schedule.append(_schedule_parse_to_model(row))
    return schedule
