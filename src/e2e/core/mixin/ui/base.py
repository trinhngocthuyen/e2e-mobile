import time

from e2e.core.ui import Button, Element, ElementCallable, TextField

from .wd import WDMixin


class BaseUIMixin(WDMixin):
    @property
    def element(self) -> ElementCallable[Element]:
        return ElementCallable(wd=self.wd, dtype=Element)

    @property
    def check(self) -> ElementCallable[Element]:
        return ElementCallable(wd=self.wd, dtype=Button, failable=True)

    @property
    def button(self) -> ElementCallable[Button]:
        return ElementCallable(wd=self.wd, dtype=Button)

    @property
    def textfield(self) -> ElementCallable[TextField]:
        return ElementCallable(wd=self.wd, dtype=TextField)

    def wait(self, seconds: float = 1):
        self.logger.debug(f'Wait for {seconds}s')
        time.sleep(seconds)
