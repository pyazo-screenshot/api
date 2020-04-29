from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

from pyazo_api.domain.pagination.dto.pagination import Pagination
from pyazo_api.util.db import get_db


class PaginationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_paginated(self, filters: (BinaryExpression), pagination: Pagination):
        objects = self.db.query(self.model)
        for filter in filters:
            objects = objects.filter(filter)
        return objects.limit(pagination.objects_per_page + 1).offset(pagination.page_number * pagination.objects_per_page).all()
