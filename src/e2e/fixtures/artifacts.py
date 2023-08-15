from datetime import datetime
from pathlib import Path

import pytest

from e2e.core.logger import logger


@pytest.fixture(scope='session')
def session_id() -> str:
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


@pytest.fixture(scope='session')
def session_artifacts_dir(session_id) -> Path:
    this = Path('.artifacts') / session_id
    this.mkdir(parents=True, exist_ok=True)
    return this


@pytest.fixture
def artifacts_dir(request, session_artifacts_dir) -> Path:
    this: Path = session_artifacts_dir / request.node.name
    this.mkdir(parents=True, exist_ok=True)
    logger.info(f'Artifacts dir: {this}')
    return this
