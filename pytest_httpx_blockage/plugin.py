from typing import Generator

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest

from pytest_httpx_blockage.blockage import blockage
from pytest_httpx_blockage.contextvar import is_blockage_enabled


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup('blockage-httpx')

    group.addoption(
        '--blockage-httpx',
        action='store_true',
        help='Block httpx requests during test run',
    )
    parser.addini(
        'blockage-httpx',
        default=False,
        help='Block httpx requests during test run',
    )

    group.addoption(
        '--disable-blockage-mark',
        action='store',
        help='If a test uses this mark, blockage would be disabled (default value is "integration")',
        default='',
    )
    parser.addini(
        'disable-blockage-mark',
        help='If a test uses this mark, blockage would be disabled (default value is "integration")',
        default='',
    )


@pytest.fixture(scope='session', autouse=True)
def _blockage(request: SubRequest) -> Generator[None, None, None]:
    config = request.config
    blockage_enabled = config.getini('blockage-httpx') or config.getoption('--blockage-httpx')

    if not blockage_enabled:
        yield
        return

    with blockage():
        yield


@pytest.fixture(autouse=True)
def _blockage_disable_mark(request: SubRequest) -> Generator[None, None, None]:
    config = request.config
    disable_mark_name = config.getini('disable-blockage-mark') or config.getoption('--disable-blockage-mark')
    mark = request.node.get_closest_marker(disable_mark_name or 'integration')
    if mark is not None:
        is_blockage_enabled.set(False)

    try:
        yield
    finally:
        is_blockage_enabled.set(True)
