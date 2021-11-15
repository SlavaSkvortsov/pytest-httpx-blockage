from contextlib import contextmanager
from typing import Generator
from unittest.mock import patch

from httpcore import Request, Response
from httpcore._async.connection import AsyncHTTPConnection
from httpcore._sync.connection import HTTPConnection

from pytest_httpx_blockage.contextvar import is_blockage_enabled
from pytest_httpx_blockage.exceptions import RequestBlockageException

base_request_sync = HTTPConnection.handle_request
base_request_async = AsyncHTTPConnection.handle_async_request


def side_effect(self: HTTPConnection, request: Request) -> Response:
    if is_blockage_enabled.get():
        raise RequestBlockageException(f'Unmocked "{request.method.decode()}" request to host="{request.url}"')
    else:
        return base_request_sync(self, request)


async def async_side_effect(self: AsyncHTTPConnection, request: Request) -> Response:
    if is_blockage_enabled.get():
        raise RequestBlockageException(f'Unmocked "{request.method.decode()}" request to host="{request.url}"')
    else:
        return await base_request_async(self, request)


@contextmanager
def blockage() -> Generator[None, None, None]:
    patch_sync = patch.object(HTTPConnection, 'handle_request', autospec=True)
    patch_async = patch.object(AsyncHTTPConnection, 'handle_async_request', autospec=True)

    with patch_sync as mocked_sync, patch_async as mocked_async:
        mocked_sync.side_effect = side_effect
        mocked_async.side_effect = async_side_effect
        yield
