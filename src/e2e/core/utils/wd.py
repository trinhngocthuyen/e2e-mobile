import base64
import typing as t

from e2e._typing import WD, Path, StrPath
from e2e.core.logger import logger

from .caps import Caps


class WDUtils:
    def __init__(self, wd: WD) -> None:
        self.wd = wd

    def take_screenshot(self, path: StrPath):
        logger.info(f'Save screenshot to: {path}')
        self.wd.save_screenshot(path)

    def save_page_source(self, path: StrPath):
        logger.info(f'Save page source to: {path}')
        Path(path).write_text(self.wd.page_source)

    def start_recording(self):
        self.wd.start_recording_screen()

    def stop_recording(self, path: StrPath):
        try:
            raw = self.wd.stop_recording_screen()
            data = base64.b64decode(raw)
            logger.info(f'Saving recording to: {path}')
            Path(path).write_bytes(data)
        except Exception as e:
            logger.warning(f'Unable to save recording. Error: {e}')

    @staticmethod
    def device_from_caps(caps: t.Dict[str, t.Any]) -> str | None:
        return Caps(caps).device

    @staticmethod
    def app_id_from_caps(caps: t.Dict[str, t.Any]) -> str | None:
        return Caps(caps).app_id
