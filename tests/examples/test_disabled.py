from httpx import Client

URL = 'https://google.com'


def test_integration() -> None:
    with Client() as client:
        response = client.get(URL)

    assert response.status_code == 200
