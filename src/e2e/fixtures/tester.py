import pytest

from e2e.tester import Tester

pytest_plugins = [
    'e2e.fixtures.core',
]


@pytest.fixture
def tester(wd):
    return Tester(wd=wd)
