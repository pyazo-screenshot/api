from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.models.image import Image
from pyazo_api.util.json_resource import JSONResource


class ImageUpload(JSONResource):
    id: str
    owner_id: int
    private: bool

    @classmethod
    def make(cls, model: Image):
        return ImageUpload(id=model.id, owner_id=model.owner_id, private=model.private)


class ImageOnShare(ImageUpload):
    owner: UserGet

    @classmethod
    def make(cls, model: Image):
        owner = UserGet(id=model.owner.id, username=model.owner.username)

        return ImageOnShare(id=model.id, owner_id=model.owner_id, private=model.private, owner=owner)
