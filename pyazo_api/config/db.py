from os import getenv


class BaseConfig:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///pyazo.db')


class TestConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')


class ProdConfig(BaseConfig):
	_DB_USER = getenv('POSTGRES_USER', 'pyazo')
	_DB_PASS = getenv('POSTGRES_PASSWORD', '')
	_DB_NAME = getenv('POSTGRES_DB', 'pyazo')
	_DB_HOST = getenv('POSTGRES_HOST', 'db')
	_DEFAULT_URI = f'postgresql://{_DB_USER}:{_DB_PASS}@{_DB_HOST}/{_DB_NAME}'
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', _DEFAULT_URI)
