from e2e._typing import WD
from e2e.core.logger import logger


class Screen:
    def __init__(self, wd: WD) -> None:
        self.wd = wd

    def wait(self, time: int = 1):
        pass

    @property
    def logger(self):
        return logger
