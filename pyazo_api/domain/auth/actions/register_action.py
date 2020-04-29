from fastapi import HTTPException
from fastapi.params import Depends

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
        user_credentials = {
            'username': register_dto.username,
            'password': register_dto.password
        }
        user_create_data = UserCreate(**user_credentials)
        existing_user = self.user_repository.get_by_username(register_dto.username)
        if existing_user:
            raise UsernameTaken()

        self.user_repository.create_user(user_create_data)

        return self.login_action(register_dto)
