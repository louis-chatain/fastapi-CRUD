from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_all_post():
    response = client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error():
    response = client.post(
        "/token",
        data={"username": "a user name that is not in the db", "password": "patate"},
    )
    access_token = response.json().get("access_token")
    assert access_token == None
    message = response.json().get("detail")
    assert message == "User not found."


def test_create_user():
    response = client.post(
        "/user/new",
        json={"username": "chat", "email": "chat", "password": "chat"},
    )
    assert response.status_code == 200
    assert response.json().get("username") == "chat"
    assert response.json().get("email") == "chat"
    assert response.json().get("id") == 1
    assert response.json().get("items") == []


def test_auth_success():
    response = client.post("/token", data={"username": "chat", "password": "chat"})
    access_token = response.json().get("access_token")
    assert access_token


def test_post_article():
    auth = client.post("/token", data={"username": "chat", "password": "chat"})
    access_token = auth.json().get("access_token")
    assert access_token

    response = client.post(
        "/article/new",
        json={
            "title": "test1",
            "content": "test2",
            "published": False,
            "creator_id": 1,
        },
        headers={"Autorization": "bearer " + access_token},
    )

    assert response.status_code == 200
    assert response.json().get("title") == "test1"
    assert response.json().get("content") == "test2"
    assert response.json().get("published") == False
    assert response.json().get("user").get("id") == 1
    assert response.json().get("user").get("username") == "chat"


def test_read_user():
    response = client.get("/user/1")
    assert response.json().get("username") == "chat"
    assert response.json().get("email") == "chat"
    assert response.json().get("id") == 1
    assert response.json().get("items")[0].get("title") == "test1"
    assert response.json().get("items")[0].get("content") == "test2"
    assert response.json().get("items")[0].get("published") == False


def test_delete_article():
    response = client.post("/article/1/delete")
    assert response.status_code == 200


def test_delete_user():
    response = client.post("/user/1/delete")
    assert response.status_code == 200