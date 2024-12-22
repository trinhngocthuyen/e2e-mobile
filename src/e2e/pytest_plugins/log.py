import pytest

from .base import Plugin


class LogPlugin(Plugin):
    @classmethod
    def load_order(cls):
        return 1e9 - 1

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        yield
        # TODO: caplog doesn't not store records after teardown
        # How to get caplog/console outputs?

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionstart(self, session):
        yield

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionfinish(self, session, exitstatus):
        yield
