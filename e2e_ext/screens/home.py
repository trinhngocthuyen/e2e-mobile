from e2e.core import Screen


class HomeScreen(Screen):
    def skip_tutorial(self):
        self.button('Skip').tap()

    def must_not_see_tutorial(self):
        self.button('Skip').must_not_exist()

    def complete_tutorial(self):
        self.element('Skip').must_exist()
        self.button('Next').tap()
        self.button('Next').tap()
        self.button('Next').tap()
        self.button('Get started').tap()

    def go_to_settings(self):
        self.button(xpath='//XCUIElementTypeButton[@label="Settings"]').tap()
