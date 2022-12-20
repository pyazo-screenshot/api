from typing import Optional

from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from pyazo_api.domain.auth.dto import User, UserCreate
from pyazo_api.domain.auth.exceptions import UsernameTaken
from pyazo_api.application.db import db


class UserRepository:
    async def get_by_username(self, username: str) -> Optional[User]:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(
                'SELECT id, username, hashed_password FROM users WHERE username = %s',
                (username,),
            )
            return await cur.fetchone()

    async def save_user(self, data: UserCreate) -> None:
        try:
            await db.execute(
                'INSERT INTO users (username, hashed_password) VALUES (%s, %s)',
                (data.username, data.hashed_password),
            )
        except UniqueViolation:
            raise UsernameTaken()
