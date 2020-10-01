import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database
from fastapi.testclient import TestClient
from PIL import Image as PILImage

from pyazo_api.run import app
from pyazo_api.application.db import Base, engine  # noqa: F401
from pyazo_api.migrate import run_migration
from pyazo_api.seed import seed
from pyazo_api.domain.images.repositories.image import ImageRepository
from pyazo_api.domain.images.repositories.share import ShareRepository

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def init_database(request):
    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)
    run_migration()
    seed()


@pytest.fixture(scope="session", autouse=True)
def image_file(request):
    im = PILImage.new(mode="RGB", size=(100, 100))
    im.save('media/test.jpg')


@pytest.fixture()
def user_token(request):
    def make_user_token(username='username1', password='password1'):
        data = {
            "username": username,
            "password": password
        }
        r = client.post("/auth/login", json=data)
        token = r.json()['access_token']
        return token

    return make_user_token


@pytest.fixture
def private_image():
    image_repository = ImageRepository()
    image = image_repository.query().filter_by('private', True).sort('created_at', order='desc').first()

    return image


@pytest.fixture
def public_image():
    image_repository = ImageRepository()
    image = image_repository.query().filter_by('private', False).sort('created_at', order='desc').first()

    return image


@pytest.fixture
def last_image():
    def get_last():
        image_repository = ImageRepository()
        return image_repository.query().sort('created_at', order='desc').first()

    return get_last


@pytest.fixture
def last_share():
    def get_last():
        share_repository = ShareRepository()
        return share_repository.query().sort('id', order='desc').first()

    return get_last
