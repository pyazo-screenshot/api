from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError

from pyazo_api.config import settings
from pyazo_api.domain.auth.dto import TokenData, User
from pyazo_api.domain.auth.exceptions import InvalidJWT
from pyazo_api.domain.auth.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(username: str) -> str:
    data = TokenData(sub=username, exp=datetime.now(UTC) + timedelta(days=7300))
    encoded_jwt = jwt.encode(
        data.model_dump(),
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


async def get_user(
    token: str,
    user_repository: UserRepository,
) -> User | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except PyJWTError as e:
        print("AAAAAAAAAAAAAAAAAA", str(e))
        return None

    try:
        data = TokenData.model_validate(payload)
    except ValidationError as e:
        print("BBBBBBBBBBBBBBBBBB", str(e))
        return None

    return await user_repository.get_by_username(data.sub)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[UserRepository, Depends()],
) -> User:
    user = await get_user(token, user_repository)
    if user is None:
        raise InvalidJWT()

    return user


async def get_current_user_or_none(
    request: Request,
    user_repository: Annotated[UserRepository, Depends()],
) -> User | None:
    try:
        token: str | None = await oauth2_scheme(request)
    except HTTPException:
        return None

    if token is None:
        return None

    return await get_user(token, user_repository)
