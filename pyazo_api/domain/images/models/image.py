from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from pyazo_api.application import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    path = Column(String)

    owner = relationship('User', back_populates='images')
