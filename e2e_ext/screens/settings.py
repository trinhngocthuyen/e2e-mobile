from e2e_ext.core import Screen


class SettingsScreen(Screen):
    def close(self):
        self.button(xpath='//XCUIElementTypeButton[@label="Close"]').tap()
