import shutil
from datetime import datetime
from pathlib import Path

import pytest
from cicd.core.logger import logger


@pytest.fixture(scope='session')
def session_id() -> str:
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


@pytest.fixture(scope='session')
def session_artifacts_dir(session_id) -> Path:
    root = Path('.artifacts')
    this = root / session_id
    this.mkdir(parents=True, exist_ok=True)
    n_sessions_to_keep = 20
    children = sorted((p for p in root.glob('*') if p.is_dir()), reverse=True)
    for dir in children[n_sessions_to_keep:]:
        logger.debug(f'Clean up old artifacts: {dir}')
        shutil.rmtree(dir)
    return this


@pytest.fixture
def artifacts_dir(request, session_artifacts_dir) -> Path:
    this: Path = session_artifacts_dir / request.node.name
    this.mkdir(parents=True, exist_ok=True)
    logger.info(f'Artifacts dir: {this}')
    return this
