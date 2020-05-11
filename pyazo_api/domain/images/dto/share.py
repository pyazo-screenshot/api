from pydantic import BaseModel

from pyazo_api.domain.images.dto.image import SharedImageResource
from pyazo_api.domain.images.models.share import Share
from pyazo_api.util.json_resource import JSONResource


class CreateShareFormSchema(BaseModel):
    image_id: str
    user_id: int


class ShareBaseResource(JSONResource):
    id: int
    image_id: str
    user_id: int
    image: SharedImageResource

    @classmethod
    def make(cls: JSONResource, model: Share):
        image = SharedImageResource.make(model.image)

        return ShareBaseResource(image=image, image_id=model.image_id, user_id=model.user_id, id=model.id)
