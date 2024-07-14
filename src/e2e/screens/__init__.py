import types
from typing import TYPE_CHECKING

from e2e._typing import WD
from e2e.core.mixin.ui import UIMixin
from e2e.core.screen import Screen
from e2e.mixin.dynamic import DynamicAttrsMixin

if TYPE_CHECKING:
    from e2e_ext._typing import ScreensTyping
else:
    ScreensTyping = types.new_class('Empty')


class Screens(
    ScreensTyping,
    DynamicAttrsMixin,
    UIMixin,
):
    def __init__(self, wd: WD, source_dir='e2e_ext/screens') -> None:
        self.wd = wd
        self.base = Screen(wd=wd)
        self.set_dynamic_attrs(
            cls=Screen,
            attr_kwargs={'wd': self.wd},
            load_source_in_dir=source_dir,
        )
