from pydantic import BaseModel


class Pagination(BaseModel):
    page_number: int
    objects_per_page: int
