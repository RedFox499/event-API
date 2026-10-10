from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_user_by_id_pass():
    response = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    response_get = client.get(
        f"/users/{response.json()['id']}"
    )
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "test"
    assert response_get.json()["email"] == "test@example.com"

def test_delete_user_by_id_pass():
    response = client.post(
        "/users",
        json={"name": "test",
              "email": "test1337@example.com"}
    )
    response_delete = client.delete(
        f"/users/{response.json()['id']}"
    )
    assert response_delete.status_code == 200
    assert response_delete.json()["name"] == "test"
    assert response_delete.json()["email"] == "test1337@example.com"

    response_get = client.get(f"/users/{response.json()['id']}")
    assert response_get.status_code == 404

def test_delete_user_by_id_fail():
    response_delete = client.delete(
        f"/users/{1999}"
    )
    assert response_delete.status_code == 404

def test_get_user_by_id_fail():
    response_get = client.get(
        f"/users/{19999}"
    )
    assert response_get.status_code == 404


def test_create_user():
    response = client.post(
        "/users",
        json={"name": "test",
        "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test"
    assert response.json()["email"] == "test@example.com"


def test_duplicate_user():
    response = client.post(
        "/users",
        json={"name": "test",
        "email": "duplicate@example.com"}
    )
    response = client.post(
        "/users",
        json={"name": "test",
              "email": "duplicate@example.com"}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"

def test_update_user_pass():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["name"] == "test"
    assert create_user.json()["email"] == "test@example.com"

    user_id = create_user.json()["id"]
    update_user = client.put(f"/users/{user_id}", json={
        "name": "new_name",
        "email": "new@example.com"
    })
    assert update_user.status_code == 200
    assert update_user.json()["name"] == "new_name"
    assert update_user.json()["email"] == "new@example.com"


def test_update_user_fail():
    update_user = client.put(f"/users/{1337}", json={
        "name": "new_name",
        "email": "new@example.com"
    })
    assert update_user.status_code == 404
    assert update_user.json()["detail"] == "User not found"

def test_update_user_same_email_fail():
    create_user1 = client.post(
        "/users",
        json={"name": "test1",
              "email": "test1@example.com"}
    )
    assert create_user1.status_code == 200
    create_user2 = client.post(
            "/users",
            json={"name": "test2",
                  "email": "test2@example.com"}
        )
    assert create_user2.status_code == 200
    user_id = create_user1.json()["id"]
    update_user1 = client.put(f"/users/{user_id}", json={
        "name": "test1",
        "email": "test2@example.com"
    })
    assert update_user1.status_code == 409
    assert update_user1.json()["detail"] == "Email already registered"

    response_get = client.get(
        f"/users/{user_id}"
    )
    assert response_get.status_code == 200
    assert response_get.json()["email"] == "test1@example.com"
