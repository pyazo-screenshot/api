import os.path

from fastapi.testclient import TestClient

from pyazo_api.config import settings
from pyazo_api.run import app

client = TestClient(app)


def test_get_images():
    r = client.get("/images")

    assert r.status_code == 401


def test_get_user_images(user_token):
    user_token = user_token()

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.get("/images", headers=headers)

    assert r.status_code == 200
    assert len(r.json()["results"]) == 2


def test_upload_image(user_token, image_file, last_image):
    user_token = user_token()

    files = {"upload_file": open(image_file, "rb")}
    headers = {"Authorization": f"Bearer {user_token}"}

    r = client.post("/images", files=files, headers=headers)

    assert r.status_code == 200

    image = last_image()
    assert os.path.isfile(os.path.join(settings.images_path, image.id))

    r = client.get("/images", headers=headers)
    assert len(r.json()["results"]) == 3


def test_upload_image_without_user(image_file):
    files = {"upload_file": open(image_file, "rb")}

    r = client.post("/images", files=files)

    assert r.status_code == 401


def test_get_public_image():
    # static serve
    pass


def test_delete_public_image_image_without_owner(user_token, public_image):
    user_token = user_token("username3", "password3")

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.delete(f"/images/{public_image.id}", headers=headers)

    assert r.status_code == 403


def test_delete_public_image_without_user(public_image):
    r = client.delete(f"/images/{public_image.id}")

    assert r.status_code == 401


def test_delete_public_image_with_owner(user_token, public_image, last_image):
    user_token = user_token()
    image = last_image()

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.delete(f"/images/{public_image.id}", headers=headers)

    assert r.status_code == 204
    assert not os.path.isfile(os.path.join(settings.images_path, image.id))
