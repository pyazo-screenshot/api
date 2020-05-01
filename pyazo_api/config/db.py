from os import getenv
import logging


class BaseConfig:
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = getenv('POSTGRES_USER', 'pyazo')
    DB_PASS = getenv('POSTGRES_PASSWORD')
    DB_NAME = getenv('POSTGRES_DB', 'pyazo')


class DevConfig(BaseConfig):
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.DEBUG)
    _DB_HOST = getenv('POSTGRES_HOST', 'localhost')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)


class TestConfig(BaseConfig):
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    _DB_HOST = getenv('POSTGRES_HOST', 'db')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)


class ProdConfig(BaseConfig):
    LOG_LEVEL = getenv('DB_LOG_LEVEL', logging.WARN)
    _DB_HOST = getenv('POSTGRES_HOST', 'db')
    _DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)
