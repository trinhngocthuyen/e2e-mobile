import pytest

from e2e._typing import WD, Path
from e2e.core.logger import logger


@pytest.fixture
def save_page_source(wd: WD, artifacts_dir):
    yield
    path: Path = artifacts_dir / 'page_source.xml'
    logger.info(f'Saving page source to: {path}')
    path.write_text(wd.page_source)
