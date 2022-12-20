from __future__ import annotations

from typing import cast, Optional
from datetime import datetime

#  from pydantic.schema import pydantic_datetime
from pydantic import BaseModel, Field

from pyazo_api.domain.auth.dto import UserGet


class Image(BaseModel):
    id: str
    owner_id: int
    private: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_tuple(cls, data: tuple[str, int, bool, datetime]) -> Image:
        return Image(
            id=data[0],
            owner_id=data[1],
            private=data[2],
            created_at=data[3],
        )
