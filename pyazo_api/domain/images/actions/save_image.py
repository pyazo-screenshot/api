import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import Depends, UploadFile

from pyazo_api.config import settings
from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.domain.images.dto import Image
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.util.http_exceptions import FileTypeException


class SaveImageAction:
    def __init__(
        self, image_repository: Annotated[ImageRepository, Depends()]
    ):
        self.image_repository: ImageRepository = image_repository

    @staticmethod
    def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()

    async def __call__(
        self,
        upload_file: UploadFile,
        clear_metadata: bool,
        uploader: UserGet,
    ) -> Image:
        id = uuid.uuid4()
        if upload_file.filename is None:
            raise FileTypeException

        extension = upload_file.filename.split(".")[-1].lower()
        if extension not in ("jpg", "jpeg", "tiff", "gif", "bmp", "png", "webp"):
            raise FileTypeException

        file_name = f"{id}.{extension}"
        relative_file_path = Path(settings.images_path) / file_name

        self.save_upload_file(upload_file, relative_file_path)

        if clear_metadata:
            subprocess.run(
                (
                    "exiftool",
                    "-overwrite_original_in_place",
                    "-all=",
                    str(relative_file_path),
                ),
                stdout=subprocess.PIPE,
            )

        img = Image(id=file_name, owner_id=uploader.id)
        await self.image_repository.save_image(img)
        return img
