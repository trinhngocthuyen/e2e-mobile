import base64
import shutil

import pytest

from e2e._typing import WD, Path
from e2e.core.logger import logger


@pytest.fixture
def screen_recording(wd: WD, artifacts_dir: Path):
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
