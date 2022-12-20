import os
from pathlib import Path
from typing import Optional

from fastapi import Depends
from starlette.responses import FileResponse

from pyazo_api.config import config
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.util.http_exceptions import NotFoundException


class GetPrivateStaticAction:
    def __init__(
        self,
        image_repository: ImageRepository = Depends(ImageRepository),
    ):
        self.image_repository = image_repository

    async def __call__(self, image_id: str, current_user: Optional[UserGet]) -> FileResponse:
        image = await self.image_repository.get_image_by_id(image_id)

        if image is None:
            raise NotFoundException

        if not current_user:
            raise NotFoundException

        if image.owner_id != current_user.id:
            raise NotFoundException

        path = Path(os.path.join(config.PRIVATE_PATH, image.id))

        return FileResponse(path, media_type="image/png")
