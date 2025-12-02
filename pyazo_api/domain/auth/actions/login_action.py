from typing import Annotated

from fastapi import Depends
from passlib.hash import argon2

from pyazo_api.domain.auth.dto import UserCredentials
from pyazo_api.domain.auth.exceptions import InvalidCredentialsException
from pyazo_api.domain.auth.repository import UserRepository
from pyazo_api.util.auth import create_access_token


class LoginAction:
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends()],
    ) -> None:
        self.user_repository: UserRepository = user_repository

    async def __call__(self, form_data: UserCredentials) -> dict[str, str]:
        user = await self.user_repository.get_by_username(form_data.username)
        if user is None or not argon2.verify(form_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        return {
            "access_token": create_access_token(user.username),
            "token_type": "bearer",
        }
