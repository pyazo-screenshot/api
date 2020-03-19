from typing import Optional
from fastapi.params import Depends
from passlib.handlers.argon2 import argon2
from sqlalchemy.orm import Session

from domain.auth.dto.user import UserCreate
from domain.auth.models.user import User
from util.db import get_db


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            hashed_password=argon2.hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
