from fastapi import APIRouter, Depends

from pyazo_api.config import config
from pyazo_api.domain.auth.actions.login_action import LoginAction
from pyazo_api.domain.auth.actions.register_action import RegisterAction
from pyazo_api.domain.auth.dto.user import UserGet, UserCredentials
from pyazo_api.domain.auth.models.user import User
from pyazo_api.util.auth import get_current_user
from pyazo_api.domain.auth.exceptions.auth import RegistrationBlocked

router = APIRouter()


@router.post('/login')
async def login(
        form_data: UserCredentials,
        login_action: LoginAction = Depends(LoginAction),
):
    return login_action(form_data)


@router.post('/register')
async def register(
        user_data: UserCredentials,
        register_action: RegisterAction = Depends(RegisterAction),
):
    if config.BLOCK_REGISTER == 'True':
        raise RegistrationBlocked
    return register_action(user_data)


@router.get('/me', response_model=UserGet)
async def get_authed_user(authed_user: User = Depends(get_current_user)):
    return UserGet(username=authed_user.username, id=authed_user.id)
