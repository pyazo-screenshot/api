import pytest
from fastapi.testclient import TestClient
from PIL import Image as PILImage

from pyazo_api.run import app
from pyazo_api.config import settings

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def image_file(tmpdir_factory):
    im = PILImage.new(mode="RGB", size=(100, 100))
    tempfile = tmpdir_factory.mktemp("images").join("test.jpg")
    im.save(str(tempfile))

    return tempfile


@pytest.fixture()
def user_token():
    def make_user_token(
        username: str = "username1", password: str = "password1"
    ) -> str:
        data = {
            "username": username,
            "password": password,
        }
        r = client.post("/auth/login", json=data)
        token = r.json()["access_token"]
        return token

    return make_user_token
