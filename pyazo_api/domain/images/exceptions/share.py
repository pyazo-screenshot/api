from fastapi import HTTPException


class ShareNotAllowedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='Share not allowed')


class ShareNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Share not found')


class DeleteShareForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='Delete share forbidden')
