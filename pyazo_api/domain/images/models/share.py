from sqlalchemy import Column, Integer, String, ForeignKey
from pyazo_api.application import Base


class Share(Base):
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String, ForeignKey('images.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
