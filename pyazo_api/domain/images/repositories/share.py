from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.orm import Session

from pyazo_api.domain.images.dto.share import ShareAdd
from pyazo_api.domain.images.models.share import Share
from pyazo_api.domain.pagination.dto.pagination import Pagination
from pyazo_api.domain.pagination.repositories.pagination import PaginationRepository
from pyazo_api.util.db import get_db


class ShareRepository(PaginationRepository):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Share

    def create_share(self, share: ShareAdd) -> Share:
        db_share = Share(
            image_id=share.image_id,
            user_id=share.user_id
        )
        self.db.add(db_share)
        self.db.commit()
        self.db.refresh(db_share)

        return db_share

    def delete(self, share: Share):
        self.db.delete(share)
        self.db.commit()

    def find_by_id(self, share_id: int) -> Optional[Share]:
        return self.db.query(Share).filter(Share.id == share_id).first()

    def get_by_user_id_and_image_id(self, user_id: int, image_id: str) -> Optional[Share]:
        return self.db.query(Share).filter(Share.image_id == image_id).filter(Share.user_id == user_id).first()

    def get_all_shares_by_user_id(self, user_id: int) -> List[Share]:
        return self.db.query(Share).filter(Share.user_id == user_id).all()

    def get_all_shares_by_user_id_paginated(self, user_id: int, pagination: Pagination) -> List[Share]:
        filters = (Share.user_id == user_id, )
        return self.get_all_paginated(filters, pagination)
