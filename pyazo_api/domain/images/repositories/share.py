from pyazo_api.domain.images.models.share import Share
from pyazo_api.util.base_repository import BaseRepository


class ShareRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Share
