from datetime import datetime
from pathlib import Path

import pytest

from e2e.core.logger import logger


@pytest.fixture(scope='session')
def session_id() -> str:
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


@pytest.fixture
def artifacts_dir(request, session_id) -> Path:
    root_dir = Path('.artifacts')
    this: Path = root_dir / session_id / request.node.name
    this.mkdir(parents=True, exist_ok=True)
    logger.info(f'Artifacts dir: {this}')
    return this
