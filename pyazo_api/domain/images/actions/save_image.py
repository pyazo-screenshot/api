import shutil
import subprocess
import uuid
import os
from pathlib import Path

from fastapi import Depends, UploadFile

from pyazo_api.config import config
from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.domain.images.dto import Image
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.util.http_exceptions import FileTypeException


class SaveImageAction:
    def __init__(self, image_repository: ImageRepository = Depends(ImageRepository)):
        self.image_repository = image_repository

    @staticmethod
    def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()

    async def __call__(self, upload_file: UploadFile, private: bool, clear_metadata: bool, uploader: UserGet) -> Image:
        random_string = uuid.uuid4()
        extension = upload_file.filename.split('.')[-1].lower()
        if extension not in ('jpg', 'jpeg', 'tiff', 'gif', 'bmp', 'png', 'webp'):
            raise FileTypeException

        file_name = f'{random_string}.{extension}'
        if private:
            relative_file_path = os.path.join(config.PRIVATE_PATH, file_name)
        else:
            relative_file_path = os.path.join(config.PUBLIC_PATH, file_name)

        destination = Path(relative_file_path)
        self.save_upload_file(upload_file, destination)

        if clear_metadata:
            subprocess.run(('exiftool', '-overwrite_original_in_place', '-all=', destination), stdout=subprocess.PIPE)

        img = Image(
            id=file_name,
            owner_id=uploader.id,
            private=private
        )
        await self.image_repository.save_image(img)
        return img
