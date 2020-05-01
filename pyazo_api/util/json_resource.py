from pydantic import BaseModel

from pyazo_api.application import Base
from pyazo_api.util.pagination import PaginatedResults


class JSONResource(BaseModel):

    @classmethod
    def make(cls: BaseModel, model: Base):
        kwargs = {
            key: getattr(model, key)
            for key in cls.dict().keys()
        }
        return cls(**kwargs)

    @classmethod
    def collection(cls, models):
        return [cls.make(model) for model in models]

    @classmethod
    def paginated_collection(cls, paginated_models: PaginatedResults):
        return {
            'results': [cls.make(model) for model in paginated_models],
            'count': paginated_models.count,
            'next_page': paginated_models.next_page
        }

