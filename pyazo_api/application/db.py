from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyazo_api.config import config
import logging

SQLALCHEMY_DATABASE_URL = config.db.SQLALCHEMY_DATABASE_URI
LOG_LEVEL = config.db.LOG_LEVEL
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(LOG_LEVEL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
