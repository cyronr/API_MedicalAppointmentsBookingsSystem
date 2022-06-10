import logging
from fastapi import FastAPI, status
from typing import List
from src.utils.db import get_db
import src.schemas.users as user_schema
import src.utils.users as user_utils

# logger = logging.getLogger('App')
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# fh = logging.FileHandler('app.log')
# fh.setLevel(logging.INFO)
# fh.setFormatter(formatter)
#
# logger.addHandler(fh)


db_log_file_name = 'db.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

db = get_db()
app = FastAPI()


@app.get("/users", response_model=List[user_schema.User])
def get_users():
    db_logger.info('Wywołanie GET/users')
    return user_utils.get_all_users(db)


@app.post("/users", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate):
    return user_utils.create_user(db, user)

