from pyazo_api.application.db import Database, db


def get_db() -> Database:
    return db
