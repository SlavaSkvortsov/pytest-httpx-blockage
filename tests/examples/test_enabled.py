import pytest
import respx as respx
from httpx import AsyncClient, Client

from pytest_httpx_blockage.exceptions import RequestBlockageException

URL = 'https://google.com'


@pytest.mark.asyncio()
async def test_async_blockage_successful() -> None:
    async with AsyncClient() as client:
        with pytest.raises(RequestBlockageException):
            await client.get(URL)


def test_sync_blockage_successful() -> None:
    with Client() as client:
        with pytest.raises(RequestBlockageException):
            client.get(URL)


@respx.mock
def test_works_with_respx() -> None:
    status_code = 418  # I'm a teapot
    respx.get(URL).respond(status_code=status_code)
    with Client() as client:
        response = client.get(URL)

    assert response.status_code == status_code


@pytest.mark.integration()
def test_integration() -> None:
    with Client() as client:
        response = client.get(URL)

    assert response.status_code == 200
