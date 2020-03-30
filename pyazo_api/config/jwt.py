from os import getenv


class BaseConfig:
	ALGORITHM = getenv('JWT_ALGORITHM', 'HS256')
	JWT_DECODE_LEEWAY = 10


class DevConfig(BaseConfig):
	SECRET = getenv('JWT_SECRET', 'secret-key')


class TestConfig(BaseConfig):
	SECRET = getenv('JWT_SECRET', 'secret-key')


class ProdConfig(BaseConfig):
	SECRET = getenv('JWT_SECRET', None)
