import pathlib

import pytest
from _pytest.fixtures import SubRequest
from _pytest.pytester import Pytester


@pytest.fixture()
def read_conftest(request: SubRequest) -> str:
    return pathlib.Path(request.config.rootdir, 'pytest_httpx_blockage/plugin.py').read_text()


def test_enabled(pytester: Pytester, read_conftest: str) -> None:
    pytester.makeconftest(read_conftest)
    pytester.copy_example()
    pytester.runpytest('--blockage-httpx').assert_outcomes(passed=4)


def test_disabled(pytester: Pytester, read_conftest: str) -> None:
    pytester.makeconftest(read_conftest)
    pytester.copy_example()
    pytester.runpytest().assert_outcomes(passed=1)
