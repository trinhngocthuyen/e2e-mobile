from e2e.core import Screen


class SettingsScreen(Screen):
    def close(self):
        self.button(xpath='//XCUIElementTypeButton[@label="Close"]').tap()
