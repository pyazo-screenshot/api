from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from pyazo_api.application import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(String, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    private = Column(Boolean, default=False)

    owner = relationship('User', back_populates='images')
    shares = relationship('Share', back_populates='image')
