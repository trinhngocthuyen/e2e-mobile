import pytest

from e2e.tester import Tester


@pytest.fixture
def tester(
    wd,
    take_screenshot,
    screen_recording,
):
    return Tester(wd=wd)
