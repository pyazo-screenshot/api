from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.util.pagination import Pagination


class GetSharesAction:
    def __init__(self, share_repository: ShareRepository = Depends()):
        self.share_repository = share_repository

    def __call__(self, current_user: UserGet, pagination: Pagination):
        return self.share_repository \
            .query() \
            .filter_by('user_id', current_user.id) \
            .load(['image.owner']) \
            .paginate(pagination)
