from os import getenv
import logging


class DBConfig:
    LOG_LEVEL: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URI: str


class BaseConfig:
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    DB_USER = getenv('POSTGRES_USER', 'pyazo')
    DB_PASS = getenv('POSTGRES_PASSWORD')
    DB_NAME = getenv('POSTGRES_DB', 'pyazo')


class DevConfig(BaseConfig):
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.DEBUG)
    _DB_HOST = getenv('POSTGRES_HOST', 'localhost')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    DATABASE_URI = getenv('DATABASE_URI', _DEFAULT_URI)


class TestConfig(BaseConfig):
    DB_NAME = getenv('POSTGRES_DB', 'pyazo_test')
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    _DB_HOST = getenv('POSTGRES_HOST', 'localhost')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    DATABASE_URI = getenv('DATABASE_URI', _DEFAULT_URI)


class ProdConfig(BaseConfig):
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    _DB_HOST = getenv('POSTGRES_HOST', 'db')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    DATABASE_URI = getenv('DATABASE_URI', _DEFAULT_URI)
