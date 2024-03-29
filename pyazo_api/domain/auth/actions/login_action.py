from fastapi import Depends
from passlib.hash import argon2

from pyazo_api.domain.auth.dto import UserCredentials
from pyazo_api.domain.auth.exceptions import InvalidCredentialsException
from pyazo_api.domain.auth.repository import UserRepository
from pyazo_api.util.auth import create_access_token


class LoginAction:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository)
    ):
        self.user_repository = user_repository

    async def __call__(self, form_data: UserCredentials):
        user = await self.user_repository.get_by_username(form_data.username)

        if user is None or not argon2.verify(form_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        token = create_access_token(
            data={'sub': user.username}
        )

        return {
            'access_token': token,
            'token_type': 'bearer'
        }
