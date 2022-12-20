from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    #  images: List


class UserCredentials(BaseModel):
    password: str
    username: str


class UserBase(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class UserGet(BaseModel):
    id: int
    username: str


class TokenResource(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
