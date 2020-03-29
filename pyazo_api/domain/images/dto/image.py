from pydantic import BaseModel


class ImageUpload(BaseModel):
    path: str
    owner_id: int


class ImageGet(ImageUpload):
    id: int
