from .base import Element


class TextField(Element):
    def input(self, value: str):
        self.tap()
        self.send_keys(value)
