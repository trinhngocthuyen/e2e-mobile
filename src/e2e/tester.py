import time
import typing as t

from e2e._typing import WD, Path
from e2e.core.mixin.ui.wd import WDMixin
from e2e.core.utils import WDUtils
from e2e.screens import Screens
from e2e.simulations import Simulations


class Tester(WDMixin):
    __test__ = False

    def __init__(self, wd: WD, **kwargs) -> None:
        self.wd = wd
        self.wd_utils = kwargs.get('wd_utils') or WDUtils(wd=wd)
        self.ui = Screens(wd=wd)
        self.simulations = Simulations()
        self.artifacts_dir: t.Optional[Path] = kwargs.get('artifacts_dir')

    def artifacts_path(self, fname: str) -> Path:
        return self.artifacts_dir / fname

    def take_screenshot(self, fname: t.Optional[str] = None):
        fname = fname or f'screenshot_{int(time.time())}.png'
        self.wd_utils.take_screenshot(self.artifacts_path(fname))

    def save_page_source(self, fname: t.Optional[str] = None):
        fname = fname or f'page_source_{int(time.time())}.xml'
        self.wd_utils.save_page_source(self.artifacts_path(fname))
