from pydantic import BaseModel


class ShareAdd(BaseModel):
    image_id: int
    user_id: int
