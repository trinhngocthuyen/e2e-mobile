import pytest

from .base import Plugin


class LogPlugin(Plugin):
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        print(
            f'--> [debug] pytest_runtest_makereport. item: {item}, nextitem: {nextitem}'
        )
        yield
        caplog = self.get_fixture(item, 'caplog')
        content = '\n'.join(
            record.msg
            for phase in ['setup', 'call', 'teardown']
            for record in caplog.get_records(phase)
            # if record.name == logger.name
        )
        print(f'--> [debug] content: {content}')
