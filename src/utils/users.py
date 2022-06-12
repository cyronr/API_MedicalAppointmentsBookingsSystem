import logging
from sqlalchemy import text
from enum import Enum
from uuid import uuid4
from src.engine.db import IsolationLevel
from src.engine.logger import get_logger_name
from src.engine.errors import ParsingError
import src.schemas.users as user_schema
import src.sql.users as user_sql

users_logger = logging.getLogger(f'{get_logger_name()}.utils.users')


class UserStatus(int, Enum):
    ACTIVE = 10
    CANCELLED = 20


class UserEventType(int, Enum):
    CREATED = 10
    MODIFIED = 20
    CANCELLED = 30


def _parse_to_model(db_row):
    try:
        user = user_schema.User(
            id=db_row['UUID'],
            email=db_row['Email'],
            typeId=db_row['TypeId']
        )
        if db_row['PersonId']:
            person_info = user_schema.PersonInfo(
                firstname=db_row['Firstname'],
                surname=db_row['Surname'],
                phone=db_row['Phone'],
                identificationNumberType=db_row['IdentificationNumberTypeId'],
                identificationNumber=db_row['IdentificationNumber'],
                city=db_row['City'],
                street=db_row['Street'],
                zipCode=db_row['ZipCode']
            )
            user.personInfo = person_info
        return user
    except Exception as err:
        msg = f'Błąd parsowania użytkownika: {err}'
        users_logger.critical(msg)
        raise ParsingError(msg)


def get_all_users(db):
    users = []
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_COMMITTED) as conn:
        result = conn.execute(text(user_sql.get_all))
        for row in result:
            users.append(_parse_to_model(row))
    return users


def get_user_by_id(db, user_id):
    try:
        with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
            result = conn.execute(
                text(user_sql.get_by_id),
                {'id': user_id}
            )
            user = result.fetchone()

            if not user:
                raise Exception(f'Brak użytkownika w bazie danych (user_id: {user_id})')

        return _parse_to_model(user)
    except Exception as err:
        users_logger.error(err)
        raise


def get_user_by_email(db, email):
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
        result = conn.execute(
            text(user_sql.get_by_email),
            {'email': email}
        )
        user = result.fetchone()

    return _parse_to_model(user) if user else None


def get_user_by_uuid(db, uuid):
    with db.connect().execution_options(isolation_level=IsolationLevel.READ_UNCOMMITTED) as conn:
        result = conn.execute(
            text(user_sql.get_by_uuid),
            {'uuid': uuid}
        )
        user = result.fetchone()

    return _parse_to_model(user) if user else None


def create_user(db, user: user_schema.UserCreate):
    internal_user = user_schema.InternalUser(
        **user.dict(),
        statusId=UserStatus.ACTIVE,
        uuid=uuid4()
    )

    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        with conn.begin():
            internal_user.id = conn.execute(
                text(user_sql.create_user),
                internal_user.dict()
            ).scalar()

            if internal_user.personInfo:
                internal_user.personId = conn.execute(
                    text(user_sql.create_person),
                    internal_user.personInfo.dict()
                ).scalar()

                conn.execute(
                    text(user_sql.update_user_by_id),
                    internal_user.dict()
                )

            conn.execute(
                text(user_sql.create_user_event),
                {
                    'user_id': internal_user.id,
                    'type_id': UserEventType.CREATED
                }
            )

            return get_user_by_id(db, internal_user.id)


def modify_user(db, user: user_schema.User):
    internal_user = user_schema.InternalUser(
        **user.dict()
    )
    internal_person_info = user_schema.InternalPersonInfo(
        **user.personInfo.dict()
    )
    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        result = conn.execute(
            text(user_sql.get_by_uuid),
            {'uuid': user.id}
        )
        dbuser = result.fetchone()
        internal_user.id = dbuser['UserId']
        internal_user.personId = dbuser['PersonId']
        internal_user.statusId = dbuser['StatusId']
        internal_person_info.personId = internal_user.personId

        with conn.begin():
            if user.personInfo:
                conn.execute(
                    text(user_sql.update_person_by_id),
                    internal_person_info.dict()
                )

            conn.execute(
                text(user_sql.update_user_by_id),
                internal_user.dict()
            )

            conn.execute(
                text(user_sql.create_user_event),
                {
                    'user_id': internal_user.id,
                    'type_id': UserEventType.MODIFIED
                }
            )
            return get_user_by_id(db, internal_user.id)


def delete_user(db, user):
    internal_user = user_schema.InternalUser(
        **user.dict()
    )
    with db.connect().execution_options(isolation_level=IsolationLevel.SERIALIZABLE) as conn:
        result = conn.execute(
            text(user_sql.get_by_uuid),
            {'uuid': user.id}
        )
        dbuser = result.fetchone()
        internal_user.id = dbuser['UserId']
        internal_user.statusId = UserStatus.CANCELLED

        with conn.begin():
            conn.execute(
                text(user_sql.update_user_by_id),
                internal_user.dict()
            )

            conn.execute(
                text(user_sql.create_user_event),
                {
                    'user_id': internal_user.id,
                    'type_id': UserEventType.CANCELLED
                }
            )
    return {}
