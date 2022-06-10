from sqlalchemy import create_engine
from enum import Enum


class IsolationLevel(str, Enum):
    AUTOCOMMIT = 'AUTOCOMMIT'
    READ_COMMITTED = 'READ COMMITTED'
    READ_UNCOMMITTED = 'READ UNCOMMITTED'
    REPEATABLE_READ = 'REPEATABLE READ'
    SERIALIZABLE = 'SERIALIZABLE'


def get_db():
    server = 'LAPTOP-TI3DHGEF'
    db_name = 'mabs'
    driver = 'ODBC Driver 17 for SQL Server'

    url = f'mssql://@{server}/{db_name}?driver={driver}'
    return create_engine(url, echo=True)