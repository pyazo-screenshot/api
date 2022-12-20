from typing import Iterator, Optional

from psycopg.rows import class_row

from pyazo_api.domain.images.dto import Image
from pyazo_api.application.db import db
from pyazo_api.util.pagination import PaginationRequest, PaginatedResults


class ImageRepository:
    async def get_image_by_id(self, image_id: str) -> Optional[Image]:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(Image)) as cur:
            await cur.execute(
                'SELECT id, owner_id, private, created_at FROM images WHERE id = %s',
                (image_id,),
            )
            return await cur.fetchone()

    async def get_paginated_images_by_owner_id(
        self,
        owner_id: int,
        pagination: PaginationRequest,
    ) -> PaginatedResults:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(Image)) as cur:
            await cur.execute(
                (
                    'SELECT id, owner_id, private, created_at '
                    'FROM images '
                    'WHERE owner_id = %s '
                    'ORDER BY created_at DESC '
                    'LIMIT %s OFFSET %s'
                ),
                (owner_id, pagination.limit, pagination.offset),

            )
            images = await cur.fetchall()
            print(owner_id)
            return PaginatedResults(
                [image for image in images],
                pagination.page + 1,
                len(images),
            )

    async def save_image(self, image: Image) -> None:
        await db.execute(
            (
                'INSERT INTO images '
                '(id, owner_id, private) '
                'VALUES '
                '(%s, %s, %s)'
            ),
            (image.id, image.owner_id, image.private),
        )

    async def delete_image_by_id(self, image_id: str) -> None:
        await db.execute(
            'DELETE FROM images WHERE id = %s',
            (image_id,),
        )
