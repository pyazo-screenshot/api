from pathlib import Path
from typing import Annotated

from fastapi import Depends

from pyazo_api.config import settings
from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.util.http_exceptions import ForbiddenException, NotFoundException


class DeleteImageAction:
    def __init__(self, image_repository: Annotated[ImageRepository, Depends()]):
        self.image_repository: ImageRepository = image_repository

    async def __call__(self, image_id: str, current_user: UserGet) -> None:
        image = await self.image_repository.get_image_by_id(image_id)
        if image is None:
            raise NotFoundException

        if image.owner_id != current_user.id:
            raise ForbiddenException

        path = Path(settings.images_path) / image.id
        path.unlink(missing_ok=True)
        await self.image_repository.delete_image_by_id(image.id)
