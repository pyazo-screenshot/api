from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.images.dto.image import ImageGet
from pyazo_api.domain.pagination.dto.pagination import Pagination


class GetSharesAction:
    def __init__(self, share_repository: ShareRepository = Depends()):
        self.share_repository = share_repository

    def image_list(self, shares):
        return [
            ImageGet(
                id=share.image.id,
            ) for share in shares.all()
        ]

    def __call__(self, current_user: UserGet, pagination: Pagination):
        shares = self.share_repository.get_all_shares_by_user_id(current_user.id)

        if pagination:
            shares, next_page = self.share_repository.paginate(shares, pagination)
            return {
                'images': self.image_list(shares),
                'next_page': next_page,
            }

        return {'images': self.image_list(shares)}
