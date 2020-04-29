from typing import List, Optional
from fastapi.params import Depends
from sqlalchemy.orm import Session

from pyazo_api.domain.images.dto.image import ImageUpload
from pyazo_api.domain.images.models.image import Image
from pyazo_api.domain.pagination.dto.pagination import Pagination
from pyazo_api.domain.pagination.repositories.pagination import PaginationRepository
from pyazo_api.util.db import get_db


class ImageRepository(PaginationRepository):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Image

    def delete(self, image: Image):
        self.db.delete(image)
        self.db.commit()

    def find_by_id(self, image_id: str) -> Optional[Image]:
        return self.db.query(Image).filter(Image.id == image_id).first()

    def get_all_by_user_id(self, user_id: int) -> List[Image]:
        return self.db.query(Image).filter(Image.owner_id == user_id).all()

    def get_all_by_user_id_paginated(self, user_id: int, pagination: Pagination) -> List[Image]:
        filters = (Image.owner_id == user_id, )
        return self.get_all_paginated(filters, pagination)

    def create_image(self, image: ImageUpload) -> Image:
        db_image = Image(
            id=image.id,
            owner_id=image.owner_id,
            private=image.private
        )
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)

        return db_image
