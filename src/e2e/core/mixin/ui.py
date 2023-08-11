from e2e.core.ui import Button, Element, ElementCallable, Textfield


class UIMixin:
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
    def textfield(self) -> ElementCallable[Textfield]:
        return ElementCallable(wd=self.wd, dtype=Textfield)
