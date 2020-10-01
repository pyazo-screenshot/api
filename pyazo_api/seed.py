import os

from pathlib import Path
from passlib.handlers.argon2 import argon2
from PIL import Image as PILImage

from pyazo_api.config import config
from pyazo_api.domain.auth.dto.user import UserCreate
from pyazo_api.domain.auth.repositories.user import UserRepository
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.dto.image import ImageBaseResource
from pyazo_api.domain.images.repositories.share import ShareRepository
from pyazo_api.domain.images.dto.share import CreateShareFormSchema


def seed_users():
    user_repository = UserRepository()

    user_repository.create(
        UserCreate(
            username='username1',
            hashed_password=argon2.hash('password1'),
        )
    )

    user_repository.create(
        UserCreate(
            username='username2',
            hashed_password=argon2.hash('password2'),
        )
    )

    user_repository.create(
        UserCreate(
            username='username3',
            hashed_password=argon2.hash('password3'),
        )
    )


def seed_images():
    image_repository = ImageRepository()

    image_repository.create(
        ImageBaseResource(
            id='1234.png',
            owner_id=1,
            private=True,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PRIVATE_PATH, '1234.png')))

    image_repository.create(
        ImageBaseResource(
            id='5678.png',
            owner_id=1,
            private=False,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PUBLIC_PATH, '5678.png')))

    image_repository.create(
        ImageBaseResource(
            id='4321.png',
            owner_id=2,
            private=True,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PRIVATE_PATH, '4321.png')))

    image_repository.create(
        ImageBaseResource(
            id='8765.png',
            owner_id=2,
            private=False,
        )
    )
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save(Path(os.path.join(config.PUBLIC_PATH, '8765.png')))


def seed_shares():
    share_repository = ShareRepository()

    share_repository.create(
        CreateShareFormSchema(
            image_id='1234.png',
            user_id=2,
        )
    )

    share_repository.create(
        CreateShareFormSchema(
            image_id='4321.png',
            user_id=3,
        )
    )


def seed():
    seed_users()
    seed_images()
    seed_shares()


if __name__ == "__main__":
    seed()
