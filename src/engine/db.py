import configparser
import logging
from urllib import parse
from sqlalchemy import create_engine
from enum import Enum
from src.engine.logger import get_logger_name

db_logger = logging.getLogger(f'{get_logger_name()}.engine.db')

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
    if config.getboolean('LOGGER', 'LogDBQuery'):
        return True
    return config.getboolean('DATABASE', 'Echo')


def get_username():
    return config.get('DATABASE', 'Username')


def get_password():
    return config.get('DATABASE', 'Password')


def get_db():
    params = parse.quote_plus(
        f'Driver={get_driver()};'
        f'Server={get_server()};'
        f'Database={get_db_name()};'
        f'Uid={get_username()}@{get_server()};'
        f'Pwd={get_password()};'
        f'Encrypt=yes;'
        f'TrustServerCertificate=no;'
        f'Connection Timeout=30;'
    )
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine = create_engine(conn_str, echo=get_echo())

    db_logger.info(f'Połączono z DB (Server = {get_server()}, DB = {get_db_name()}, Echo = {get_echo()})')
    return engine
