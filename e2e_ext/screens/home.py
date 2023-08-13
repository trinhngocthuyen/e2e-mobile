from e2e.core.screen import Screen


class HomeScreen(Screen):
    def skip_tutorial(self):
        self.button('Skip').tap()

    def complete_tutorial(self):
        self.element('Skip').must_exist()
        self.button('Next').tap()
        self.button('Next').tap()
        self.button('Next').tap()
        self.button('Get started').tap()

    def go_to_settings(self):
        self.logger.debug('Go to settings')
