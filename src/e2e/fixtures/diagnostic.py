import base64
import shutil

import pytest
from cicd.core.logger import logger

from e2e._typing import WD, Path
from e2e.core.utils import WDUtils


@pytest.fixture
def diagnostic(
    save_caplog,
    save_screen_recording,
    save_page_source,
    save_screenshot,
):
    pass


@pytest.fixture
def save_screenshot(wd_utils: WDUtils, artifacts_dir):
    yield
    wd_utils.take_screenshot(artifacts_dir / 'screenshot.png')


@pytest.fixture
def save_page_source(wd_utils: WDUtils, artifacts_dir):
    yield
    wd_utils.save_page_source(artifacts_dir / 'page_source.xml')


@pytest.fixture
def save_screen_recording(wd: WD, artifacts_dir: Path):
    if not shutil.which('ffmpeg'):
        logger.warning(
            'Skip recording screen because `ffmpeg` was not installed. '
            'To install it, run `brew install ffmpeg`.'
        )
        yield
        return

    wd.start_recording_screen()
    yield
    try:
        path = artifacts_dir / 'recording.mp4'
        raw = wd.stop_recording_screen()
        data = base64.b64decode(raw)
        logger.info(f'Saving recording to: {path}')
        path.write_bytes(data)
    except Exception as e:
        logger.warning(f'Unable to save recording. Error: {e}')


@pytest.fixture
def save_caplog(
    caplog,
    artifacts_dir,
):
    yield
    path: Path = artifacts_dir / 'caplog.txt'
    logger.info(f'Saving caplog to: {path}')
    content = '\n'.join(
        record.msg
        for phase in ['setup', 'call', 'teardown']
        for record in caplog.get_records(phase)
        if record.name == logger.name
    )
    path.write_text(content)
