from typing import Annotated

from fastapi import APIRouter, Depends

from pyazo_api.config import settings
from pyazo_api.domain.auth.actions.login_action import LoginAction
from pyazo_api.domain.auth.actions.register_action import RegisterAction
from pyazo_api.domain.auth.dto import User, UserCredentials, UserGet
from pyazo_api.domain.auth.exceptions import RegistrationBlocked
from pyazo_api.util.auth import get_current_user

router = APIRouter()


@router.post("/login")
async def login(
    form_data: UserCredentials,
    login_action: Annotated[LoginAction, Depends()],
) -> dict[str, str]:
    return await login_action(form_data)


@router.post("/register")
async def register(
    user_data: UserCredentials,
    register_action: Annotated[RegisterAction, Depends()],
) -> dict[str, str]:
    if settings.block_register:
        raise RegistrationBlocked
    return await register_action(user_data)


@router.get("/me", response_model=UserGet)
async def get_authed_user(
    authed_user: Annotated[User, Depends(get_current_user)],
) -> UserGet:
    return authed_user.to_public()
