from typing import List, Optional, Any

from pyazo_api.application import Base
from pyazo_api.util.pagination import Pagination


class QueryBuilder:
    def __init__(self, query, repo):
        self.query = query
        self.repo = repo

    def __getattribute__(self, function):
        if function in ('repo', 'query'):
            return object.__getattribute__(self, function)

        def execute(*args, **kwargs):
            repo_function = getattr(self.repo, function)
            results = repo_function(self.query, *args, **kwargs)
            return results

        if function in ('all', 'paginate', 'first'):
            return execute

        def add_to_query(*args, **kwargs):
            repo_function = getattr(self.repo, function)
            self.query = repo_function(self.query, *args, **kwargs)
            return self

        return add_to_query

    def filter_by(self, field: str, value: Any) -> 'QueryBuilder':
        pass

    def load(self, relations: List[str]) -> 'QueryBuilder':
        pass

    def paginate(self, pagination: Pagination) -> 'QueryBuilder':
        pass

    def all(self) -> List[Base]:
        pass

    def first(self) -> Optional[Base]:
        pass
