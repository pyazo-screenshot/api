from pydantic import BaseModel


class ImageUpload(BaseModel):
    id: str
    owner_id: int
    private: bool


class ImageGet(BaseModel):
    id: str
