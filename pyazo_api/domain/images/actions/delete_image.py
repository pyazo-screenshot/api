import os

from pathlib import Path
from fastapi.params import Depends

from pyazo_api.config import config
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.util.http_exceptions import NotFoundException, ForbiddenException


class DeleteImageAction:
    def __init__(self, image_repository: ImageRepository = Depends()):
        self.image_repository = image_repository

    def __call__(self, image_id: str, current_user: UserGet):
        image = self.image_repository \
            .query() \
            .filter_by('id', image_id) \
            .first()
        if not image:
            raise NotFoundException

        if not image.owner.id == current_user.id:
            raise ForbiddenException

        if image.private:
            path = Path(os.path.join(config.PRIVATE_PATH, image.id))
        else:
            path = Path(os.path.join(config.PUBLIC_PATH, image.id))

        path.unlink(missing_ok=True)
        self.image_repository.delete(image)
