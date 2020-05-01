from typing import Any, Optional, List
from fastapi.params import Depends
from sqlalchemy import orm
from sqlalchemy.orm import Session, Query
from pydantic import BaseModel

from pyazo_api.application import Base
from pyazo_api.domain.images.repositories.query_builder import QueryBuilder
from pyazo_api.util.pagination import Pagination, PaginatedResults
from pyazo_api.util.db import get_db


class BaseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        if isinstance(db, Depends):
            self.db = db.dependency().__next__()
        else:
            self.db = db

        self.model = None

    def query(self) -> QueryBuilder:
        query = self.db.query(self.model)

        return QueryBuilder(query, self)

    def load(self, query_builder: Query, relations: List[str]) -> Query:
        return query_builder.options(
            [orm.joinedload(relation) for relation in relations]
        )

    def filter(self, query_builder: Query, condition) -> Query:
        return query_builder.filter(condition)

    def filter_by(self, query_builder: Query, field: str, value: Any) -> Query:
        return query_builder.filter(getattr(self.model, field) == value)

    def all(self, query_builder: Query) -> List[Base]:
        return query_builder.all()

    def first(self, query_builder: Query) -> Optional[Base]:
        return query_builder.first()

    def first_or_create(self, values: BaseModel, match: Optional[dict] = None) -> Base:
        match = match or values.dict()
        query = self.db.query(self.model)
        for key, value in match.items():
            query = query.filter(getattr(self.model, key) == value)

        return query.first() or self.create(values)

    def paginate(self, query_builder, pagination: Pagination):
        next_page = None
        objects = query_builder \
            .limit(pagination.per_page + 1) \
            .offset(pagination.page * pagination.per_page) \
            .all()
        if len(objects) > pagination.per_page:
            objects = objects[:-1]
            next_page = pagination.page + 1

        count = query_builder.count() if pagination.with_count else None

        return PaginatedResults(results=objects, next_page=next_page, count=count)

    def create(self, data: BaseModel) -> Base:
        db_entity = self.model(**data.dict())
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)

        return db_entity

    def delete(self, entity: Base) -> None:
        self.db.delete(entity)
        self.db.commit()
