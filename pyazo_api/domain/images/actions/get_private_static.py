from typing import Optional
from pathlib import Path

from fastapi.params import Depends

from pyazo_api.config import config
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.auth.dto.user import UserGet
from starlette.responses import FileResponse

from pyazo_api.util.http_exceptions import NotFoundException


class GetPrivateStaticAction:
    def __init__(
        self,
        image_repository: ImageRepository = Depends(ImageRepository),
        share_repository: ShareRepository = Depends()
    ):
        self.image_repository = image_repository
        self.share_repository = share_repository

    def __call__(self, image_id: str, current_user: Optional[UserGet]):
        image = self.image_repository \
            .query() \
            .filter_by('id', image_id) \
            .first()
        if not image:
            raise NotFoundException

        if not current_user:
            raise NotFoundException

        if image.owner_id != current_user.id:
            share = self.share_repository \
                .query() \
                .filter_by('user_id', current_user.id) \
                .filter_by('image_id', image_id) \
                .first()
            if not share:
                raise NotFoundException

        path = Path(f'{config.PRIVATE_PATH}{image.id}')

        return FileResponse(path, media_type="image/png")
