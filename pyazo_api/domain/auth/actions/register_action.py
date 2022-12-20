from fastapi import Depends
from passlib.handlers.argon2 import argon2

from pyazo_api.domain.auth.actions.login_action import LoginAction
from pyazo_api.domain.auth.dto import UserCreate, UserCredentials
from pyazo_api.domain.auth.repository import UserRepository
from pyazo_api.domain.auth.exceptions import UsernameTaken


class RegisterAction:
    def __init__(
        self,
        login_action: LoginAction = Depends(LoginAction),
        user_repository: UserRepository = Depends(UserRepository)
    ):
        self.login_action = login_action
        self.user_repository = user_repository

    async def __call__(self, register_dto: UserCredentials):
        user_create_data = UserCreate(
            username=register_dto.username,
            hashed_password=argon2.hash(register_dto.password)
        )
        await self.user_repository.save_user(user_create_data)

        return await self.login_action(register_dto)
