from contextlib import contextmanager
from typing import Any, Dict, Generator, Tuple
from unittest.mock import patch

from httpcore import AsyncByteStream, SyncByteStream
from httpcore._async.connection import AsyncHTTPConnection
from httpcore._sync.connection import SyncHTTPConnection
from httpcore._types import URL, Headers

from pytest_httpx_blockage.contextvar import is_blockage_enabled
from pytest_httpx_blockage.exceptions import RequestBlockageException

base_request_sync = SyncHTTPConnection.handle_request
base_request_async = AsyncHTTPConnection.handle_async_request


def side_effect(
    self: SyncHTTPConnection,
    method: bytes,
    url: URL,
    *args: Any,
    **kwargs: Any,
) -> Tuple[int, Headers, SyncByteStream, Dict[Any, Any]]:
    if is_blockage_enabled.get():
        raise RequestBlockageException(f'Unmocked "{method.decode()}" request to host="{url}"')
    else:
        return base_request_sync(
            self,
            method,
            url,
            *args,
            **kwargs,
        )


async def async_side_effect(
    self: AsyncHTTPConnection,
    method: bytes,
    url: URL,
    *args: Any,
    **kwargs: Any,
) -> Tuple[int, Headers, AsyncByteStream, Dict[Any, Any]]:
    if is_blockage_enabled.get():
        raise RequestBlockageException(f'Unmocked "{method.decode()}" request to host="{url}"')
    else:
        return await base_request_async(
            self,
            method,
            url,
            *args,
            **kwargs,
        )


@contextmanager
def blockage() -> Generator[None, None, None]:
    patch_sync = patch.object(SyncHTTPConnection, 'handle_request', autospec=True)
    patch_async = patch.object(AsyncHTTPConnection, 'handle_async_request', autospec=True)

    with patch_sync as mocked_sync, patch_async as mocked_async:
        mocked_sync.side_effect = side_effect
        mocked_async.side_effect = async_side_effect
        yield
