from fastapi.params import Depends
from sqlalchemy.orm import Session

from pyazo_api.domain.images.dto.share import ShareAdd
from pyazo_api.domain.images.models.share import Share
from pyazo_api.util.db import get_db


class ShareRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_share(self, share: ShareAdd) -> Share:
        db_share = Share(
            image_id=share.image_id,
            user_id=share.user_id
        )
        self.db.add(db_share)
        self.db.commit()
        self.db.refresh(db_share)

    def get_by_user_id_and_image_id(self, user_id: int, image_id: int):
        print(user_id, image_id)
        return self.db.query(Share).filter(Share.image_id == image_id).filter(Share.user_id == user_id).first()
