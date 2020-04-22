import shutil
import subprocess
import uuid
from pathlib import Path

from fastapi import UploadFile
from fastapi.params import Depends

from pyazo_api.domain.auth.dto.user import UserGet
from pyazo_api.domain.images.exceptions.image import FileTypeException
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

    def __call__(self, upload_file: UploadFile, private: bool, clear_metadata: bool, uploader: UserGet):
        random_string = uuid.uuid4()
        extension = upload_file.filename.split('.')[-1].lower()
        if extension not in ('jpg', 'jpeg', 'tiff', 'gif', 'bmp', 'png', 'webp'):
            raise FileTypeException

        file_name = f'{random_string}.{extension}'
        relative_file_path = f'./public/images/{file_name}'
        destination = Path(relative_file_path).relative_to(Path('./'))
        self.save_upload_file(upload_file, destination)

        if clear_metadata:
            subprocess.run(('exiftool', '-overwrite_original_in_place', '-all=', destination), stdout=subprocess.PIPE)

        return self.image_repository.create_image(
            ImageUpload(
                id=file_name,
                owner_id=uploader.id,
                private=private
            )
        )
