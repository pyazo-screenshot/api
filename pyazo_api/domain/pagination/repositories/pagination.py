from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

from pyazo_api.domain.pagination.dto.pagination import Pagination
from pyazo_api.util.db import get_db


class PaginationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def paginate(self, objects, pagination: Pagination):
        next_page = False
        objects = objects.limit(pagination.objects_per_page + 1).offset(pagination.page_number * pagination.objects_per_page)
        if objects.count() > pagination.objects_per_page:
            objects = objects[:-1]
            next_page = True
        return objects, next_page
