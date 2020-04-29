from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.dto.image import ImageGet
from pyazo_api.domain.pagination.dto.pagination import Pagination


class GetImagesAction:
    def __init__(self, image_repository: ImageRepository = Depends()):
        self.image_repository = image_repository

    def image_list(self, images):
        return [
            ImageGet(
                id=image.id,
            ) for image in images.all()
        ]

    def __call__(self, current_user: UserGet, pagination: Pagination):
        images = self.image_repository.get_all_by_user_id(current_user.id)

        if pagination:
            images, next_page = self.image_repository.paginate(images, pagination)
            return {
                'images': self.image_list(images),
                'next_page': next_page,
            }

        return {'images': self.image_list(images)}
