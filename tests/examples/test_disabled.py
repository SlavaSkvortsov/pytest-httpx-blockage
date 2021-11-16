from httpx import Client

URL = 'https://httpbin.org/status/200'


def test_integration() -> None:
    with Client() as client:
        response = client.get(URL)

    assert response.status_code == 200
