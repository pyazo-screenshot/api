from os import getenv
from typing import cast

from pyazo_api.config.db import DBConfig
from pyazo_api.config.jwt import JWTConfig


class Config:
    db: DBConfig
    jwt: JWTConfig
    ENV: str
    DEBUG: bool
    TESTING: bool
    LOGGING_LEVEL: str
    APP_URL: str
    BLOCK_REGISTER: bool
    PUBLIC_PATH: str
    PRIVATE_PATH: str


class DevConfig(Config):
    from .jwt import DevConfig as jwt
    from .db import DevConfig as db
    ENV = 'development'
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = 'DEBUG'
    APP_URL = getenv('APP_URL', 'localhost')
    BLOCK_REGISTER = bool(getenv('BLOCK_REGISTER', False))
    PUBLIC_PATH = getenv('PUBLIC_PATH', './media/public/')
    PRIVATE_PATH = getenv('PRIVATE_PATH', './media/private/')


class TestConfig():
    from .jwt import TestConfig as jwt
    from .db import TestConfig as db
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = 'INFO'
    APP_URL = getenv('APP_URL', 'pyazo-testing')
    BLOCK_REGISTER = bool(getenv('BLOCK_REGISTER', False))
    PUBLIC_PATH = getenv('PUBLIC_PATH', './media/public/')
    PRIVATE_PATH = getenv('PRIVATE_PATH', './media/private/')


class ProdConfig():
    from .jwt import ProdConfig as jwt
    from .db import ProdConfig as db
    ENV = 'production'
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = 'WARNING'
    APP_URL = getenv('APP_URL', None)
    BLOCK_REGISTER = bool(getenv('BLOCK_REGISTER', False))
    PUBLIC_PATH = getenv('PUBLIC_PATH', './media/public/')
    PRIVATE_PATH = getenv('PRIVATE_PATH', './media/private/')


configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
}

environment = getenv('ENV', 'production')
config = cast(Config, configs.get(environment, ProdConfig))
