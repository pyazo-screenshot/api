from pathlib import Path
from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.share import ShareNotFoundException
from pyazo_api.domain.images.repositories.share import ShareRepository


class DeleteShareAction:
    def __init__(self, share_repository: ShareRepository = Depends()):
        self.share_repository = share_repository

    def __call__(self, share_id: int):
        share = self.share_repository.find_by_id(share_id)
        if not share:
            raise ShareNotFoundException

        self.share_repository.delete(share)
