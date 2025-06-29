from http import HTTPStatus


def test_root_returns_message(client):
    # client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, World!"}
