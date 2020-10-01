import os.path

from fastapi.testclient import TestClient

from pyazo_api.config import config
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
    assert len(r.json()['results']) == 2


def test_upload_image(user_token, last_image):
    user_token = user_token()

    files = {'upload_file': open('media/test.jpg', 'rb')}
    headers = {"Authorization": f"Bearer {user_token}"}

    r = client.post("/images", files=files, headers=headers)

    assert r.status_code == 200

    image = last_image()
    assert os.path.isfile(os.path.join(config.PUBLIC_PATH, image.id))

    r = client.get("/images", headers=headers)
    assert len(r.json()['results']) == 3


def test_upload_private_image(user_token, last_image):
    user_token = user_token()

    files = {'upload_file': open('media/test.jpg', 'rb')}
    headers = {"Authorization": f"Bearer {user_token}"}
    params = {"private": True}
    r = client.post("/images", files=files, headers=headers, params=params)

    assert r.status_code == 200

    image = last_image()
    assert os.path.isfile(os.path.join(config.PRIVATE_PATH, image.id))

    r = client.get("/images", headers=headers)
    assert len(r.json()['results']) == 4


def test_upload_image_without_user():

    files = {'upload_file': open('media/test.jpg', 'rb')}

    r = client.post("/images", files=files)

    assert r.status_code == 401


def test_get_private_image(user_token, private_image):
    user_token = user_token()

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.get(f"/{private_image.id}", headers=headers)

    assert r.status_code == 200


def test_get_private_image_without_user(private_image):
    r = client.get(f"/{private_image.id}")

    assert r.status_code == 404


def test_get_public_image():
    # static serve
    pass


def test_delete_private_image_image_without_owner(user_token, private_image):
    user_token = user_token("username3", "password3")

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.delete(f"/images/{private_image.id}", headers=headers)

    assert r.status_code == 403


def test_delete_private_image_with_owner(user_token, private_image, last_image):
    user_token = user_token()
    image = last_image()

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.delete(f"/images/{private_image.id}", headers=headers)

    assert r.status_code == 204
    assert not os.path.isfile(os.path.join(config.PRIVATE_PATH, image.id))


def test_delete_private_image_with_shares(user_token):
    user3_token = user_token('username3', 'password3')
    headers3 = {"Authorization": f"Bearer {user3_token}"}
    r = client.get("/shares", headers=headers3)
    shares1 = len(r.json()['results'])

    user2_token = user_token('username2', 'password2')

    headers2 = {"Authorization": f"Bearer {user2_token}"}
    r = client.delete("/images/4321.png", headers=headers2)

    assert r.status_code == 204
    assert not os.path.isfile(os.path.join(config.PRIVATE_PATH, "4321.png"))

    r = client.get("/shares", headers=headers3)
    shares2 = len(r.json()['results'])
    assert shares1 > shares2


def test_delete_private_image_without_user(private_image):
    r = client.delete(f"/images/{private_image.id}")

    assert r.status_code == 401


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
    assert not os.path.isfile(os.path.join(config.PRIVATE_PATH, image.id))
