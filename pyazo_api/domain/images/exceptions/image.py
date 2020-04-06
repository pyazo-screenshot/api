from fastapi import HTTPException


class ImageNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Image not found')


class DeleteImageForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='Delete image forbidden')
