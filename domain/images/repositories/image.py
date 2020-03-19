from typing import List
from fastapi.params import Depends
from sqlalchemy.orm import Session

from domain.images.dto.image import ImageUpload
from domain.images.models.image import Image
from util.db import get_db


class ImageRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_by_user_id(self, user_id: int) -> List[Image]:
        return self.db.query(Image).filter(Image.owner_id == user_id).all()

    def create_image(self, image: ImageUpload) -> Image:
        db_image = Image(
            path=image.path,
            owner_id=image.owner_id
        )
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)

        return db_image
