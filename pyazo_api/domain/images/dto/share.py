from pydantic import BaseModel


class ShareAdd(BaseModel):
    image_id: str
    user_id: int
