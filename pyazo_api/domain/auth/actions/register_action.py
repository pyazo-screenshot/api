from fastapi import Depends
from passlib.handlers.argon2 import argon2

from pyazo_api.domain.auth.actions.login_action import LoginAction
from pyazo_api.domain.auth.dto.user import UserCreate, UserCredentials
from pyazo_api.domain.auth.repositories.user import UserRepository
from pyazo_api.domain.auth.exceptions.auth import UsernameTaken


class RegisterAction:
    def __init__(
        self,
        login_action: LoginAction = Depends(LoginAction),
        user_repository: UserRepository = Depends(UserRepository)
    ):
        self.login_action = login_action
        self.user_repository = user_repository

    def __call__(self, register_dto: UserCredentials):
        user_create_data = UserCreate(
            username=register_dto.username,
            hashed_password=argon2.hash(register_dto.password)
        )
        existing_user = self.user_repository \
            .query() \
            .filter_by('username', register_dto.username) \
            .first()
        if existing_user:
            raise UsernameTaken()

        self.user_repository.create(user_create_data)

        return self.login_action(register_dto)
