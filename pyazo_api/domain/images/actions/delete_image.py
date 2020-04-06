from pathlib import Path
from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.image import ImageNotFoundException
from pyazo_api.domain.images.repositories.image import ImageRepository


class DeleteImageAction:
    def __init__(self, image_repository: ImageRepository = Depends(ImageRepository)):
        self.image_repository = image_repository

    def __call__(self, image_id: str):
        image = self.image_repository.find_by_id(image_id)
        if not image:
            raise ImageNotFoundException

        path = Path(f'./public/images/{image.id}')
        path.unlink(missing_ok=True)
        self.image_repository.delete(image)
