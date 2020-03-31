from os import getenv


class BaseConfig:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DB_USER = getenv('POSTGRES_USER', 'pyazo')
	DB_PASS = getenv('POSTGRES_PASSWORD')
	DB_NAME = getenv('POSTGRES_DB', 'pyazo')


class DevConfig(BaseConfig):
	_DB_HOST = getenv('POSTGRES_HOST', 'localhost')
	_DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)


class TestConfig(BaseConfig):
	_DB_HOST = getenv('POSTGRES_HOST', 'db')
	_DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)


class ProdConfig(BaseConfig):
	_DB_HOST = getenv('POSTGRES_HOST', 'db')
	_DEFAULT_URI = f'postgresql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASS}@{_DB_HOST}/{BaseConfig.DB_NAME}'
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)
