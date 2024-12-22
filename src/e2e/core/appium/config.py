from urllib.parse import urlparse

import pytest


class AppiumConfig:
    def __init__(self, **kwargs):
        self.server_url: str = kwargs.get('server_url', 'http://127.0.0.1:4723')
        cmps = urlparse(self.server_url)
        self.host = cmps.hostname
        self.port = cmps.port
        self.origin = f'{cmps.scheme}://{self.host}:{self.port}'

    @staticmethod
    def from_pytest_config(config: pytest.Config):
        return AppiumConfig(server_url=config.option.appium)
