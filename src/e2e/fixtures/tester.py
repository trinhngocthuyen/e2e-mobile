import pytest

from e2e import Tester


@pytest.fixture
def tester(
    wd,
    artifacts_dir,
    diagnostic,
):
    return Tester(wd=wd, artifacts_dir=artifacts_dir)
