from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pyazo_api.config import config

SQLALCHEMY_DATABASE_URL = config.db.SQLALCHEMY_DATABASE_URI
LOG_LEVEL = config.db.LOG_LEVEL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
