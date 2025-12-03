from collections.abc import Iterator

from pydantic import BaseModel
from starlette.requests import Request


class PaginationRequest:
    page: int
    limit: int
    with_count: bool

    def __init__(self, page: int = 0, limit: int = 1000, with_count: bool = False):
        limit = 1000 if limit > 1000 else limit
        self.page = page
        self.with_count = with_count
        self.limit = limit

    @property
    def offset(self) -> int:
        return self.page * self.limit


class PaginatedResults[T](BaseModel):
    results: list[T]
    count: int
    next_page: int

    def get_results(self) -> Iterator[T]:
        for result in self.results:
            yield result


async def extract_pagination(request: Request) -> PaginationRequest:
    query_params = request.query_params

    return PaginationRequest(
        page=int(query_params.get('page', 0)),
        limit=int(query_params.get('limit', 50)),
        with_count=bool(query_params.get('with_count', False))
    )
