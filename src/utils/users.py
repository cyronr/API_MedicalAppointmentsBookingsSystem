import logging
from sqlalchemy import text
from enum import Enum
from src.utils.db import IsolationLevel
import src.schemas.users as user_schema
import src.sql.users as user_sql

users_logger = logging.getLogger('sqlalchemy.utils.users')


class UserStatus(int, Enum):
    ACTIVE = 1
    CANCELLED = 2


class UserEventType(int, Enum):
    CREATED = 1
    MODIFIED = 2


def _parse_to_model(db_row):
    return user_schema.User(
            id=db_row["Id"],
            email=db_row["Email"],
            uuid=db_row["UUID"]
        )


def get_all_users(db):
    users_logger.info('start')
    users = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(text(user_sql.get_all))
        for row in result:
            users.append(_parse_to_model(row))
    users_logger.info('end')
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
    internal_user = user_schema.UserInternal(**user.dict())
    internal_user.status_id = UserStatus.ACTIVE

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
