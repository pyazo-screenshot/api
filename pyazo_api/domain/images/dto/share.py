from pydantic import BaseModel

from pyazo_api.domain.images.dto.image import ImageOnShare
from pyazo_api.domain.images.models.share import Share
from pyazo_api.util.json_resource import JSONResource


class ShareAdd(BaseModel):
    image_id: str
    user_id: int


class ShareGet(JSONResource):
    id: int
    image_id: str
    user_id: int
    image: ImageOnShare

    @classmethod
    def make(cls: JSONResource, model: Share):
        image = ImageOnShare.make(model.image)

        return ShareGet(image=image, image_id=model.image_id, user_id=model.user_id, id=model.id)
