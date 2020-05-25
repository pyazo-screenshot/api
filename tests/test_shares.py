from fastapi.testclient import TestClient

from pyazo_api.run import app


client = TestClient(app)


def test_get_user1_shares(user_token):
    user_token = user_token()

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.get("/shares", headers=headers)

    assert r.status_code == 200
    assert len(r.json()['results']) == 0


def test_get_user3_shares(user_token):
    user_token = user_token('username2', 'password2')

    headers = {"Authorization": f"Bearer {user_token}"}
    r = client.get("/shares", headers=headers)

    assert r.status_code == 200
    assert len(r.json()['results']) == 1


def test_share_image_owner(user_token, private_image):
    user_token = user_token()

    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"image_id": "1234.png", "user_id": "3"}
    r = client.post("/shares", headers=headers, json=data)

    assert r.status_code == 200


def test_share_image_not_owner(user_token, private_image):
    user_token = user_token('username2', 'password2')

    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"image_id": "1234.png", "user_id": "3"}
    r = client.post("/shares", headers=headers, json=data)

    assert r.status_code == 403


def test_share_image_without_user(user_token, private_image):
    user_token = user_token()

    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"image_id": "1234.png", "user_id": "4"}
    r = client.post("/shares", headers=headers, json=data)

    assert r.status_code == 404


def test_delete_share_without_user(last_share):
    share = last_share()
    r = client.delete(f"/shares/{share.id}")

    assert r.status_code == 401


def test_delete_share_without_owner(user_token, last_share):
    user_token = user_token('username2', 'password2')
    share = last_share()

    headers = {"Authorization": f"Bearer {user_token}"}

    r = client.delete(f"/shares/{share.id}", headers=headers)

    assert r.status_code == 403


def test_delete_share(user_token, last_share):
    user_token = user_token()
    share = last_share()

    headers = {"Authorization": f"Bearer {user_token}"}

    r = client.delete(f"/shares/{share.id}", headers=headers)

    assert r.status_code == 204
