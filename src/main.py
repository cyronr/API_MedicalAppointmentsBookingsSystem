from fastapi import FastAPI, status
from typing import List
from src.engine.db import get_db
from src.engine.logger import get_logger, get_dblogger
import src.schemas.users as user_schema
import src.utils.users as user_utils
import configparser


logger = get_logger()
get_dblogger()
db = get_db()
app = FastAPI()

logger.info('Application Startup')
config = configparser.ConfigParser()


@app.get('/')
def main():
    return {"Hello": "API"}


@app.get("/users", response_model=List[user_schema.User])
def get_users():
    return user_utils.get_all_users(db)


@app.post("/users", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate):
    return user_utils.create_user(db, user)

