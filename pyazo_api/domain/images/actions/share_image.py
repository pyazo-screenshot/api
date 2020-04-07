from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.image import ImageNotFoundException
from pyazo_api.domain.images.exceptions.share import ShareNotAllowedException
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.images.dto.share import ShareAdd
from pyazo_api.domain.auth.exceptions.auth import UserNotFoundException
from pyazo_api.domain.auth.repositories.user import UserRepository
from pyazo_api.domain.auth.dto.user import UserGet, UserBase


class ShareImageAction:
    def __init__(self, image_repository: ImageRepository = Depends(), user_repository: UserRepository = Depends(), share_repository: ShareRepository = Depends()):
        self.image_repository = image_repository
        self.user_repository = user_repository
        self.share_repository = share_repository

    def __call__(self, image_id: str, share_with: UserBase, user: UserGet):
        image = self.image_repository.find_by_id(image_id)
        if not image:
            raise ImageNotFoundException

        if image.owner_id != user.id:
            raise ShareNotAllowedException

        share_with = self.user_repository.get_by_username(share_with.username)
        if not share_with:
            raise UserNotFoundException

        share = self.share_repository.get_by_user_id_and_image_id(share_with.id, image.id)
        if share:
            raise ShareNotAllowedException

        return self.share_repository.create_share(
            ShareAdd(
                image_id=image.id,
                user_id=share_with.id
            )
        )
