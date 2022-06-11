import configparser
from sqlalchemy import create_engine
from enum import Enum

config = configparser.ConfigParser()
config.read('app.ini')


class IsolationLevel(str, Enum):
    AUTOCOMMIT = 'AUTOCOMMIT'
    READ_COMMITTED = 'READ COMMITTED'
    READ_UNCOMMITTED = 'READ UNCOMMITTED'
    REPEATABLE_READ = 'REPEATABLE READ'
    SERIALIZABLE = 'SERIALIZABLE'


def get_server():
    return config.get('DATABASE', 'Server')


def get_db_name():
    return config.get('DATABASE', 'DBName')


def get_driver():
    return config.get('DATABASE', 'Driver')


def get_echo():
    return config.getboolean('DATABASE', 'Echo')


def get_db():
    url = f'mssql://@{get_server()}/{get_db_name()}?driver={get_driver()}'
    return create_engine(url, echo=get_echo())
