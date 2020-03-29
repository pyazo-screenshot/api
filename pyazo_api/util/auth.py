from datetime import timedelta, datetime
import jwt
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from pyazo_api.config.jwt import SECRET, ALGORITHM
from pyazo_api.domain.auth.dto.user import TokenData
from pyazo_api.domain.auth.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7300)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repository: UserRepository = Depends(UserRepository)
):
    try:
        payload = jwt.decode(token, SECRET, ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            return None
        token_data = TokenData(username=username)
    except PyJWTError:
        return None
    user = user_repository.get_by_username(username=token_data.username)

    return user
