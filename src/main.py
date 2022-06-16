from fastapi import FastAPI, status, HTTPException
from starlette.responses import RedirectResponse
from typing import List
from src.engine.db import get_db
from src.engine.logger import get_logger, get_dblogger
import src.engine.errors as errors
import src.schemas.users as user_schema
import src.utils.users as user_utils


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
    return user_utils.get_all_users(db)


@app.get('/users/{userId}', response_model=user_schema.User)
def get_user(user_id):
    try:
        user = user_utils.get_user_by_uuid(db, user_id)
        if not user:
            raise errors.NotFound('Brak użytkownika')
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
            raise errors.NotFound('Brak użytkownika')

        return user_utils.modify_user(db, user)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.delete('/users/{userId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id):
    try:
        user = user_utils.get_user_by_uuid(db, user_id)
        if not user:
            raise errors.NotFound('Brak użytkownika')

        return user_utils.delete_user(db, user)
    except errors.NotFound as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
