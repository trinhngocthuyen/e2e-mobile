import typing as t

from cicd.core.logger import logger

from e2e._typing import WD, Path, StrPath

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

    @staticmethod
    def device_from_caps(caps: t.Dict[str, t.Any]) -> str | None:
        return Caps(caps).device

    @staticmethod
    def app_id_from_caps(caps: t.Dict[str, t.Any]) -> str | None:
        return Caps(caps).app_id
