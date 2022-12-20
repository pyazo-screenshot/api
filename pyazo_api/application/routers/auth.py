from fastapi import APIRouter, Depends

from pyazo_api.config import config
from pyazo_api.domain.auth.actions.login_action import LoginAction
from pyazo_api.domain.auth.actions.register_action import RegisterAction
from pyazo_api.domain.auth.dto import User, UserGet, UserCredentials
from pyazo_api.util.auth import get_current_user
from pyazo_api.domain.auth.exceptions import RegistrationBlocked

router = APIRouter()


@router.post('/login', tags=["auth"])
async def login(
    form_data: UserCredentials,
    login_action: LoginAction = Depends(LoginAction),
):
    return await login_action(form_data)


@router.post('/register', tags=["auth"])
async def register(
    user_data: UserCredentials,
    register_action: RegisterAction = Depends(RegisterAction),
):
    if config.BLOCK_REGISTER == 'True':
        raise RegistrationBlocked
    return await register_action(user_data)


@router.get('/me', response_model=UserGet, tags=["auth"])
async def get_authed_user(authed_user: User = Depends(get_current_user)):
    return UserGet(username=authed_user.username, id=authed_user.id)
