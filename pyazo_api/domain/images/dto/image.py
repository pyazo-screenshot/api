from pydantic import BaseModel


class ImageUpload(BaseModel):
    path: str
    owner_id: int
    private: bool


class ImageGet(ImageUpload):
    id: int
