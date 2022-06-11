import logging
from pydantic import ValidationError
from sqlalchemy import text
from enum import Enum
from uuid import uuid4
from src.engine.db import IsolationLevel
from src.engine.logger import get_logger_name
import src.schemas.users as user_schema
import src.sql.users as user_sql

users_logger = logging.getLogger(f'{get_logger_name()}.utils.users')


class UserStatus(int, Enum):
    ACTIVE = 1
    CANCELLED = 2


class UserEventType(int, Enum):
    CREATED = 1
    MODIFIED = 2


def _parse_to_model(db_row):
    try:
        return user_schema.User(
            id=db_row["Id"],
            email=db_row["Email"],
            uuid=db_row["UUID"]
        )
    except Exception as err:
        users_logger.critical(f'Błąd parsowania użytkownika: {err}')
        raise


def get_all_users(db):
    users = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(text(user_sql.get_all))
        for row in result:
            users.append(_parse_to_model(row))
    return users


def get_user_by_id(db, user_id):
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(
            text(user_sql.get_by_id),
            {"user_id": user_id}
        )
        user = result.fetchone()
    return _parse_to_model(user)


def create_user(db, user: user_schema.UserCreate):
    internal_user = user_schema.UserInternal(
        **user.dict(),
        status_id=UserStatus.ACTIVE,
        uuid=uuid4()
    )

    with db.connect().execution_options(isolation_level=IsolationLevel.REPEATABLE_READ) as conn:
        with conn.begin():
            user_id = conn.execute(
                text(user_sql.create_user),
                internal_user.dict()
            ).scalar()

            conn.execute(
                text(user_sql.create_event),
                {
                    "user_id": user_id,
                    "type_id": UserEventType.CREATED
                }
            )
    return get_user_by_id(db, user_id)
