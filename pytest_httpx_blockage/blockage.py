from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import patch

from httpcore._async.connection import AsyncHTTPConnection
from httpcore._sync.connection import SyncHTTPConnection
from httpx import URL

from pytest_httpx_blockage.exceptions import RequestBlockageException


def side_effect(
    method: bytes,
    url: URL,
    *args: Any,
    **kwargs: Any,
) -> None:
    raise RequestBlockageException(f'Unmocked "{method.decode()}" request to host="{url}"')


async def async_side_effect(
    method: bytes,
    url: URL,
    *args: Any,
    **kwargs: Any,
) -> None:
    side_effect(method=method, url=url)


@contextmanager
def blockage() -> Generator[None, None, None]:
    patch_sync = patch.object(SyncHTTPConnection, 'request')
    patch_async = patch.object(AsyncHTTPConnection, 'arequest')
    with patch_sync as mocked_sync, patch_async as mocked_async:
        mocked_sync.side_effect = side_effect
        mocked_async.side_effect = async_side_effect
        yield
