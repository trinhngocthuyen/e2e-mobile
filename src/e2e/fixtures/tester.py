import pytest

from e2e.tester import Tester


@pytest.fixture
def tester(
    wd,
    save_page_source,
    screen_recording,
    take_screenshot,
):
    return Tester(wd=wd)
