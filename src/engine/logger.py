import configparser
import logging

config = configparser.ConfigParser()
config.read('app.ini')


def get_logger_name():
    return config.get('LOGGER', 'Name')


def get_filename():
    return config.get('LOGGER', 'FileName')


def get_level():
    match config.get('LOGGER', 'Level'):
        case 'DEBUG':
            return logging.DEBUG
        case 'INFO':
            return logging.INFO
        case 'WARNING':
            return logging.WARNING
        case 'ERROR':
            return logging.ERROR
        case 'CRITICAL':
            return logging.CRITICAL
        # default
        case _:
            return logging.ERROR


def get_formatter():
    return logging.Formatter(' %(asctime)s | %(name)s | %(levelname)s | %(message)s')


def get_file():
    logger_file = logging.FileHandler(get_filename())
    logger_file.setLevel(get_level())
    logger_file.setFormatter(get_formatter())
    return logger_file


def get_logger():
    logger = logging.getLogger(get_logger_name())
    logger.addHandler(get_file())
    logger.setLevel(get_level())
    return logger


def get_dblogger():
    if config.getboolean('LOGGER', 'LogDBQuery'):
        logger = logging.getLogger('sqlalchemy')
        logger.addHandler(get_file())
        logger.setLevel(get_level())
        return logger
    else:
        return None
