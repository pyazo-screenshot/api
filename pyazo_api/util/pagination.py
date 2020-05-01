from typing import List, Optional

from starlette.requests import Request
from pyazo_api.application import Base


class Pagination:
    page: int
    per_page: int
    with_count: bool

    def __init__(self, page: int = 0, per_page: int = 1000, with_count: bool = False):
        per_page = 1000 if per_page > 1000 else per_page
        self.page = page
        self.with_count = with_count
        self.per_page = per_page


class PaginatedResults:
    def __init__(self, results: List[Base], next_page: int, count: Optional[int] = None):
        self.results = results
        self.next_page = next_page
        self.count = count

    def __iter__(self):
        for result in self.results:
            yield result


async def extract_pagination(
    request: Request,
):
    query_params = request.query_params

    return Pagination(
        page=int(query_params.get('page', 0)),
        per_page=int(query_params.get('per_page', 50)),
        with_count=bool(query_params.get('with_count', False))
    )
