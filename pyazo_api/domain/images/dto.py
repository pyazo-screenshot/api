from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Image(BaseModel):
    id: str
    owner_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_tuple(cls, data: tuple[str, int, datetime]) -> Image:
        return Image(
            id=data[0],
            owner_id=data[1],
            created_at=data[2],
        )
