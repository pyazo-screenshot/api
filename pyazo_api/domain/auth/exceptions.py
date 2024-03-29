from fastapi import HTTPException


class InvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Invalid credentials')


class InvalidJWT(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Invalid access token')


class UserNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='User not found')


class RegistrationBlocked(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=403, detail='Registration disabled')


class UsernameTaken(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail='Username already registered')
