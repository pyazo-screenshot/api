from typing import Optional

from pydantic.schema import datetime

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.models.image import Image
from pyazo_api.util.json_resource import JSONResource


class ImageBaseResource(JSONResource):
    id: str
    owner_id: int
    private: bool
    # TODO: remove optional after separating FormRequests and DTOs
    created_at: Optional[datetime]

    @classmethod
    def make(cls, model: Image):
        return ImageBaseResource(
            id=model.id,
            owner_id=model.owner_id,
            private=model.private,
            created_at=model.created_at
        )


class SharedImageResource(ImageBaseResource):
    owner: UserGet

    @classmethod
    def make(cls, model: Image):
        owner = UserGet(id=model.owner.id, username=model.owner.username)

        return SharedImageResource(id=model.id, owner_id=model.owner_id, private=model.private, owner=owner)
