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
            "published": True,
            "creator_id": 3,
        },
        headers={"Autorization": "bearer " + access_token}
    )

    assert response.status_code==200
    assert response.json().get("title") == "test1"
    assert response.json().get("content") == "test2"
    assert response.json().get("published") == True
    assert response.json().get("user").get("id") == 3
    assert response.json().get("user").get("username") == "chat"