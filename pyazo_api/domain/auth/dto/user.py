from typing import List

from pydantic import BaseModel


class UserCredentials(BaseModel):
    password: str
    username: str


class UserBase(BaseModel):
    username: str


class User(UserBase):
    pass


class UserCreate(UserBase):
    hashed_password: str


class UserGet(User):
    id: int
    username: str


class UserInDB(User):
    id: int
    hashed_password: str
    images: List

    class Config:
        orm_mode = True


class TokenResource(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
