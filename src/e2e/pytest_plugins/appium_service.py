from functools import cached_property

import pytest
import requests
from appium.webdriver.appium_service import AppiumService

from e2e.core.logger import logger

from .base import Plugin


class AppiumServicePlugin(Plugin):
    service: AppiumService | None = None

    @classmethod
    def load_order(cls):
        return 1e9 - 1

    @cached_property
    def appium_log_path(self):
        return self.session_artifacts_dir / 'appium.log'

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionstart(self, session):
        if self.is_non_exec_session(session):
            yield
            return
        if not session.config.option.appium_server_auto or self.is_server_up():
            yield
            return

        logger.info(f'Appium server was not up. Will start Appium at: {self.appium_config.server_url}')
        self.service = AppiumService()
        with self.appium_log_path.open('wb') as f:
            self.service.start(
                args=[
                    '--address',
                    self.appium_config.host,
                    '--port',
                    str(self.appium_config.port),
                ],
                stdout=f,
                stderr=f,
                timeout_ms=20000,
            )
        yield

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionfinish(self, session, exitstatus):
        yield
        if self.service:
            logger.info(f'Stop Appium service at: {self.appium_config.server_url}')
            self.service.stop()

    def is_server_up(self):
        try:
            response = requests.get(f'{self.appium_config.server_url}/status', timeout=5)
            return response.json().get('value').get('ready')
        except:
            pass
