from psycopg.rows import class_row

from pyazo_api.application.db import get_pool
from pyazo_api.domain.images.dto import Image
from pyazo_api.util.pagination import PaginatedResults, PaginationRequest


class ImageRepository:
    async def get_image_by_id(self, image_id: str) -> Image | None:
        async with get_pool().connection() as conn:
            async with conn.cursor(row_factory=class_row(Image)) as cur:
                await cur.execute(
                    "SELECT id, owner_id, created_at FROM images WHERE id = %s",
                    (image_id,),
                )
                return await cur.fetchone()

    async def get_paginated_images_by_owner_id(
        self,
        owner_id: int,
        pagination: PaginationRequest,
    ) -> PaginatedResults:
        async with get_pool().connection() as conn:
            async with conn.cursor(row_factory=class_row(Image)) as cur:
                await cur.execute(
                    (
                        "SELECT id, owner_id, created_at "
                        "FROM images "
                        "WHERE owner_id = %s "
                        "ORDER BY created_at DESC "
                        "LIMIT %s OFFSET %s"
                    ),
                    (owner_id, pagination.limit, pagination.offset),
                )
                images = await cur.fetchall()
                return PaginatedResults(
                    results=list(images),
                    next_page=pagination.page + 1,
                    count=len(images),
                )

    async def save_image(self, image: Image) -> None:
        async with get_pool().connection() as conn:
            await conn.execute(
                ("INSERT INTO images (id, owner_id) VALUES (%s, %s)"),
                (image.id, image.owner_id),
            )

    async def delete_image_by_id(self, image_id: str) -> None:
        async with get_pool().connection() as conn:
            await conn.execute(
                "DELETE FROM images WHERE id = %s",
                (image_id,),
            )
