from e2e.core.screen import Screen


class HomeScreen(Screen):
    def go_to_settings(self):
        self.logger.debug('Go to settings')
