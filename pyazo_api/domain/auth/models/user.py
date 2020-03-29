from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from pyazo_api.application.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    images = relationship('Image', back_populates='owner')
