from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.models.image import Image
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.util.pagination import Pagination


class GetImagesAction:
    def __init__(
        self,
        image_repository: ImageRepository = Depends(ImageRepository),
    ):
        self.image_repository = image_repository

    def __call__(self, owner: UserGet, pagination: Pagination):
        return self.image_repository \
            .query() \
            .filter(Image.owner_id == owner.id) \
            .sort(field='created_at', order='desc') \
            .paginate(pagination)
