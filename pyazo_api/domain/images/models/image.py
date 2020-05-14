import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from pyazo_api.application import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(String, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship('User', back_populates='images')
    shares = relationship('Share', back_populates='image')
