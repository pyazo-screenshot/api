#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD 3-Clause license.

from os import getenv


class DevConfig():
	from .jwt import DevConfig as jwt
	from .db import DevConfig as db
	DEBUG = True
	TESTING = True
	LOGGING_LEVEL = 'DEBUG'
	APP_URL = getenv('APP_URL', 'localhost')


class TestConfig():
	from .jwt import TestConfig as jwt
	from .db import TestConfig as db
	DEBUG = True
	TESTING = True
	LOGGING_LEVEL = 'INFO'
	APP_URL = getenv('APP_URL', 'pyazo-testing')


class ProdConfig():
	from .jwt import ProdConfig as jwt
	from .db import ProdConfig as db
	DEBUG = False
	TESTING = False
	LOGGING_LEVEL = 'WARNING'
	APP_URL = getenv('APP_URL', None)


configs = {
	'development': DevConfig,
	'testing': TestConfig,
	'production': ProdConfig,
}

environment = getenv('ENV', 'production')
config = configs.get(environment, ProdConfig)
