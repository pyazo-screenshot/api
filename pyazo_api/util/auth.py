from datetime import timedelta, datetime

import jwt
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from pyazo_api.config import config
from pyazo_api.domain.auth.dto.user import TokenData
from pyazo_api.domain.auth.repositories.user import UserRepository
from pyazo_api.domain.auth.exceptions.auth import InvalidJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7300)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, config.jwt.SECRET, algorithm=config.jwt.ALGORITHM)

    return encoded_jwt


async def get_user(
        token: str,
        user_repository: UserRepository
):
    try:
        payload = jwt.decode(token, config.jwt.SECRET, algorithm=config.jwt.ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            return None
        token_data = TokenData(username=username)
    except PyJWTError:
        return None
    user = user_repository.query() \
        .filter_by('username', username) \
        .first()

    return user


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repository: UserRepository = Depends(UserRepository)
):
    user = await get_user(token, user_repository)
    if user is None:
        raise InvalidJWT()

    return user


async def get_current_user_or_none(
        request: Request,
        user_repository: UserRepository = Depends(UserRepository)
):
    try:
        token: str = await oauth2_scheme(request)
    except HTTPException:
        return None

    return await get_user(token, user_repository)
