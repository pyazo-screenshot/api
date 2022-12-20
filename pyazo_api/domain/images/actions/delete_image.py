import os
from pathlib import Path

from fastapi import Depends

from pyazo_api.config import config
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.util.http_exceptions import NotFoundException, ForbiddenException


class DeleteImageAction:
    def __init__(self, image_repository: ImageRepository = Depends()):
        self.image_repository = image_repository

    async def __call__(self, image_id: str, current_user: UserGet) -> None:
        image = await self.image_repository.get_image_by_id(image_id)
        if image is None:
            raise NotFoundException

        if not image.owner_id == current_user.id:
            raise ForbiddenException

        if image.private:
            path = Path(os.path.join(config.PRIVATE_PATH, image.id))
        else:
            path = Path(os.path.join(config.PUBLIC_PATH, image.id))

        path.unlink(missing_ok=True)
        await self.image_repository.delete_image_by_id(image.id)
