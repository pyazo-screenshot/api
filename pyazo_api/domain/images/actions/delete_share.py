from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.share import ShareNotFoundException, DeleteShareForbiddenException
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.auth.dto.user import UserGet


class DeleteShareAction:
    def __init__(self, share_repository: ShareRepository = Depends()):
        self.share_repository = share_repository

    def __call__(self, share_id: int, current_user: UserGet):
        share = self.share_repository.find_by_id(share_id)
        if not share:
            raise ShareNotFoundException

        if not share.image.owner.id == current_user.id:
            raise DeleteShareForbiddenException

        self.share_repository.delete(share)
