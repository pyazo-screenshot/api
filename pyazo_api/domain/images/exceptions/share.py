from fastapi import HTTPException


class ShareNotAllowedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='Share not allowed')
