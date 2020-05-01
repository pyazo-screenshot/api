from pyazo_api.domain.images.models.image import Image
from pyazo_api.util.base_repository import BaseRepository


class ImageRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Image
