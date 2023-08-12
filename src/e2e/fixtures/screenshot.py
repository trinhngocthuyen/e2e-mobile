import pytest

from e2e._typing import WD
from e2e.core.logger import logger


@pytest.fixture
def take_screenshot(wd: WD, artifacts_dir):
    yield
    path = artifacts_dir / 'screenshot.png'
    logger.info(f'Saving screenshot to: {path}')
    wd.save_screenshot(path)
