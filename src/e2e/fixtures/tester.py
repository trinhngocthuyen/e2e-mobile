import pytest

from e2e.tester import Tester


@pytest.fixture
def tester(wd, take_screenshot):
    yield Tester(wd=wd)
