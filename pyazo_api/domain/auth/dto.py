from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str

    def to_public(self) -> "UserGet":
        return UserGet(id=self.id, username=self.username)


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
    sub: str
    exp: datetime
