import asyncio
import os

from pathlib import Path
from passlib.handlers.argon2 import argon2
from PIL import Image as PILImage

from pyazo_api.config import config
from pyazo_api.domain.auth.dto import UserCreate
from pyazo_api.domain.auth.repository import UserRepository
from pyazo_api.domain.images.repository import ImageRepository
from pyazo_api.domain.images.dto import Image


async def seed_users():
    user_repository = UserRepository()

    await user_repository.save_user(
        UserCreate(
            username='username1',
            hashed_password=argon2.hash('password1'),
        )
    )

    await user_repository.save_user(
        UserCreate(
            username='username2',
            hashed_password=argon2.hash('password2'),
        )
    )

    await user_repository.save_user(
        UserCreate(
            username='username3',
            hashed_password=argon2.hash('password3'),
        )
    )


async def seed_images():
    image_repository = ImageRepository()

    await image_repository.save_image(
        Image(
            id='1234.png',
            owner_id=1,
            private=True,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PRIVATE_PATH, '1234.png')))

    await image_repository.save_image(
        Image(
            id='5678.png',
            owner_id=1,
            private=False,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PUBLIC_PATH, '5678.png')))

    await image_repository.save_image(
        Image(
            id='4321.png',
            owner_id=2,
            private=True,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PRIVATE_PATH, '4321.png')))

    await image_repository.save_image(
        Image(
            id='8765.png',
            owner_id=2,
            private=False,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PUBLIC_PATH, '8765.png')))


async def seed():
    await seed_users()
    await seed_images()


if __name__ == "__main__":
    asyncio.run(seed())
