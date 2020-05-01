from pyazo_api.domain.images.models.image import Image
from pyazo_api.util.json_resource import JSONResource


class ImageUpload(JSONResource):
    id: str
    owner_id: int
    private: bool

    @classmethod
    def make(cls, model: Image):
        return ImageUpload(id=model.id, owner_id=model.owner_id, private=model.private)
