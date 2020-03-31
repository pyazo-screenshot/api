import shutil
import string
import random
from pathlib import Path
from fastapi import UploadFile
from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.dto.image import ImageUpload
from pyazo_api.domain.images.repositories.image import ImageRepository


class SaveImageAction:
    def __init__(self, image_repository: ImageRepository = Depends(ImageRepository)):
        self.image_repository = image_repository

    @staticmethod
    def save_upload_file(upload_file: UploadFile, destination: Path):
        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()

    def __call__(self, upload_file: UploadFile, private: bool, uploader: UserGet):
        random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
        extension = upload_file.filename.split('.')[-1]
        file_name = f'{random_string}.{extension}'
        relative_file_path = f'./public/images/{file_name}'
        destination = Path(relative_file_path)
        self.save_upload_file(upload_file, destination.relative_to(Path('./')))

        return self.image_repository.create_image(
            ImageUpload(
                owner_id=uploader.id,
                path=file_name,
                private=private
            )
        )
