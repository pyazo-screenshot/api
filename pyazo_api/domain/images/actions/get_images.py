from typing import Annotated
from fastapi import Depends

from pyazo_api.domain.auth.dto import UserGet
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.util.pagination import PaginationRequest, PaginatedResults


class GetImagesAction:
    def __init__(self, image_repository: Annotated[ImageRepository, Depends()]):
        self.image_repository: ImageRepository = image_repository

    async def __call__(self, owner: UserGet, pagination: PaginationRequest) -> PaginatedResults:
        return await self.image_repository.get_paginated_images_by_owner_id(owner.id, pagination)
