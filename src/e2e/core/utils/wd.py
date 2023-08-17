import typing as t

from e2e._typing import WD, Path, StrPath
from e2e.core.logger import logger


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
    def device_from_caps(caps: t.Optional[t.Dict[str, t.Any]]) -> t.Optional[str]:
        keys = ['udid', 'appium:udid', 'deviceName', 'appium:deviceName']
        return next((caps[k] for k in keys if k in caps), None)
