from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_404_NOT_FOUND


class NotFoundException(HTTPException):
    def __init__(self, detail: str = 'Not found') -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = 'Action forbidden') -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)


class FileTypeException(HTTPException):
    def __init__(self, detail: str = 'File type not supported') -> None:
        super().__init__(status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail)
