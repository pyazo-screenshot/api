from fastapi.params import Depends

from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.util.http_exceptions import NotFoundException, ForbiddenException


class DeleteShareAction:
    def __init__(self, share_repository: ShareRepository = Depends()):
        self.share_repository = share_repository

    def __call__(self, share_id: int, current_user: UserGet):
        share = self.share_repository \
            .query() \
            .filter_by('id', share_id) \
            .first()
        if not share:
            raise NotFoundException

        if not share.image.owner.id == current_user.id:
            raise ForbiddenException

        self.share_repository.delete(share)
