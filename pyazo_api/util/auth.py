from datetime import timedelta, datetime
from typing import Any, Optional

import jwt
from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from pyazo_api.config import config
from pyazo_api.domain.auth.dto import TokenData, User
from pyazo_api.domain.auth.repository import UserRepository
from pyazo_api.domain.auth.exceptions import InvalidJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def create_access_token(*, data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7300)
    encoded_jwt = jwt.encode(
        {
            **data,
            'exp': expire,
        },
        config.jwt.SECRET,
        algorithm=config.jwt.ALGORITHM,
    )

    return encoded_jwt


async def get_user(
    token: str,
    user_repository: UserRepository,
) -> Optional[User]:
    try:
        payload = jwt.decode(token, config.jwt.SECRET, algorithms=[config.jwt.ALGORITHM])
        username: str = str(payload.get('sub'))
        if username is None:
            return None
        token_data = TokenData(username=username)
    except PyJWTError as e:
        return None

    return await user_repository.get_by_username(username)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(UserRepository)
) -> User:
    user = await get_user(token, user_repository)
    if user is None:
        raise InvalidJWT()

    return user


async def get_current_user_or_none(
    request: Request,
    user_repository: UserRepository = Depends(UserRepository)
) -> Optional[User]:
    try:
        token: Optional[str] = await oauth2_scheme(request)
    except HTTPException:
        return None

    if token is None:
        return None

    return await get_user(token, user_repository)
