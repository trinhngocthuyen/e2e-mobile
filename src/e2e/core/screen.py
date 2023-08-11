from e2e._typing import WD
from e2e.core.logger import logger
from e2e.core.mixin.ui import UIMixin


class Screen(UIMixin):
    def __init__(self, wd: WD) -> None:
        self.wd = wd

    def wait(self, time: int = 1):
        pass

    @property
    def logger(self):
        return logger
