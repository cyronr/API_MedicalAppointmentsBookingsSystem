from fastapi import FastAPI, status, HTTPException
from starlette.responses import RedirectResponse
from typing import List
from src.engine.db import get_db
from src.engine.logger import get_logger, get_dblogger
import src.engine.errors as errors
import src.schemas.users as user_schema
import src.utils.users as user_utils
import src.schemas.doctors as doctor_schema
import src.utils.doctors as doctor_utils
import src.schemas.bookings as booking_schema
import src.utils.bookings as booking_utils


logger = get_logger()
logger.info('Application Startup')

db_logger = get_dblogger()
db = get_db()
app = FastAPI()


@app.get('/')
def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get('/users', response_model=List[user_schema.User])
def get_users():
    try:
        return user_utils.get_all_users(db)
    except Exception as err:
        logger.error(err)
        raise


@app.get('/users/{userId}', response_model=user_schema.User)
def get_user(user_id):
    try:
        user = user_utils.get_user_by_uuid(db, user_id)
        if not user:
            raise errors.NotFound('Brak użytkownika o podanym identyfikatorze')
        return user
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.post('/users', response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate):
    try:
        if user_utils.get_user_by_email(db, user.email):
            raise errors.UserAlreadyExists('Użytkownik z podanym mailem już istnieje')

        return user_utils.create_user(db, user)
    except errors.UserAlreadyExists as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@app.put('/users', response_model=user_schema.User)
def modify_user(user: user_schema.User):
    try:
        if not user_utils.get_user_by_uuid(db, user.id):
            raise errors.NotFound('Brak użytkownika o podanym identyfikatorze')

        return user_utils.modify_user(db, user)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.delete('/users/{userId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id):
    try:
        user = user_utils.get_user_by_uuid(db, user_id)
        if not user:
            raise errors.NotFound('Brak użytkownika o podanym identyfikatorze')

        return user_utils.delete_user(db, user)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.get('/users/{userId}/bookings', response_model=List[booking_schema.Booking])
def get_bookings_by_user(user_id):
    try:
        return booking_utils.get_bookings_by_user(db, user_id)
    except Exception as err:
        logger.error(err)
        raise


@app.get('/doctors', response_model=List[doctor_schema.Doctor])
def get_doctors():
    try:
        return doctor_utils.get_all_doctors(db)
    except Exception as err:
        logger.error(err)
        raise


@app.get('/doctors/{doctorId}', response_model=doctor_schema.Doctor)
def get_doctor(doctor_id):
    try:
        doctor = doctor_utils.get_doctor_by_uuid(db, doctor_id)
        if not doctor:
            raise errors.NotFound('Brak lekarza o podanym identyfikatorze')
        return doctor
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.get('/doctors/{doctorId}/schedule', response_model=List[doctor_schema.Schedule])
def get_doctor_schedule(doctor_id):
    try:
        doctor = doctor_utils.get_doctor_by_uuid(db, doctor_id)
        if not doctor:
            raise errors.NotFound('Brak lekarza o podanym identyfikatorze')
        return doctor_utils.get_doctor_schedule(db, doctor)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.post('/bookings', response_model=booking_schema.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: booking_schema.BookingCreate):
    try:
        return booking_utils.create_booking(db, booking)
    except Exception as err:
        logger.error(err)
        raise


@app.post('/bookings/{bookingId}/confirm', response_model=booking_schema.Booking, status_code=status.HTTP_201_CREATED)
def confirm_booking(booking_id):
    try:
        booking = booking_utils.get_booking_by_uuid(db, booking_id)
        if not booking:
            raise errors.NotFound('Brak rezerwacji o podanym identyfikatorze')
        return booking_utils.confirm_booking(db, booking)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.delete('/bookings/{bookingId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id):
    try:
        booking = booking_utils.get_booking_by_uuid(db, booking_id)
        if not booking:
            raise errors.NotFound('Brak rezerwacji o podanym identyfikatorze')
        return booking_utils.delete_booking(db, booking_id)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
