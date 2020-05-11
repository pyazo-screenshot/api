from fastapi.params import Depends

from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.images.dto.share import CreateShareFormSchema
from pyazo_api.domain.auth.exceptions.auth import UserNotFoundException
from pyazo_api.domain.auth.repositories.user import UserRepository
from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.util.http_exceptions import NotFoundException, ForbiddenException


class ShareImageAction:
    def __init__(
        self,
        image_repository: ImageRepository = Depends(),
        user_repository: UserRepository = Depends(),
        share_repository: ShareRepository = Depends()
    ):
        self.image_repository = image_repository
        self.user_repository = user_repository
        self.share_repository = share_repository

    def __call__(self, share_data: CreateShareFormSchema, user: UserGet):
        image = self.image_repository \
            .query() \
            .filter_by('id', share_data.image_id) \
            .first()
        if not image:
            raise NotFoundException

        if image.owner_id != user.id:
            raise ForbiddenException

        share_with = self.user_repository \
            .query() \
            .filter_by('id', share_data.user_id) \
            .first()
        if not share_with:
            raise UserNotFoundException

        return self.share_repository \
            .first_or_create(
                match={
                    'user_id': share_data.user_id,
                    'image_id': share_data.image_id,
                },
                values=share_data
            )
