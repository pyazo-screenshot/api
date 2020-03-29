from pyazo_api.application.db import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
