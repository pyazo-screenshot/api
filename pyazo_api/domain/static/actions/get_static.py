# from pathlib import Path
from fastapi.params import Depends

from pyazo_api.domain.images.exceptions.image import ImageNotFoundException
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.auth.dto.user import UserGet
from starlette.responses import FileResponse


class GetStaticAction:
    def __init__(self, image_repository: ImageRepository = Depends(ImageRepository)):
        self.image_repository = image_repository

    def __call__(self, image_path: str, uploader: UserGet):
        image = self.image_repository.find_by_path(image_path)
        if not image:
            raise ImageNotFoundException

        if image.private:
            raise ImageNotFoundException
        return FileResponse("public/images/" + image_path, media_type="image/png")
