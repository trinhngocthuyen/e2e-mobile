import logging
import typing as t

import pytest

from e2e.core.logger import compact_logger, logger

from .base import Plugin


class SessionFileHandler(logging.FileHandler):
    pass


class ItemFileHandler(logging.FileHandler):
    pass


class LogPlugin(Plugin):
    separator = '-' * 80

    @classmethod
    def load_order(cls):
        return 1e9 - 1

    @property
    def session_log_path(self):
        return self.session_artifacts_dir / 'pytest.log'

    @property
    def item_log_path(self):
        return self.artifacts_dir / 'pytest.log'

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        self.add_log_handler(self.item_log_path, dtype=ItemFileHandler)
        compact_logger.info(f'\n{self.separator}')
        logger.info(f'Test started: {item.nodeid}\n{self.separator}')
        yield
        self.remove_log_handler(dtype=ItemFileHandler)

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        # Workaround to add line break after the log of node id
        # https://github.com/pytest-dev/pytest/issues/8574#issuecomment-828756544
        compact_logger.debug('')

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        def excinfo_to_str(excinfo: pytest.ExceptionInfo):
            try:
                return str(excinfo.getrepr(style='native').reprcrash)
            except:
                return excinfo.exconly()

        yield
        if call.excinfo:
            logger.error(
                f'Test failed: {item.nodeid}\n'
                f'{self.separator}\n'
                f'{excinfo_to_str(call.excinfo)}\n'
                f'{self.separator}'
            )

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_logreport(self, report):
        yield
        # Workaround to make test result (PASSED/FAILED/ERROR) printed in a newline
        # Note that if a test enters `teardown` phase, it already succeeded in `call` phase
        if report.outcome in {'error', 'failed'} or report.when == 'teardown':
            compact_logger.debug('')

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionstart(self, session):
        if not self.is_non_exec_session(session):
            self.add_log_handler(path=self.session_log_path, dtype=SessionFileHandler)
        yield

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionfinish(self, session, exitstatus):
        yield
        if not self.is_non_exec_session(session):
            self.remove_log_handler(dtype=SessionFileHandler)

    def add_log_handler(self, path, dtype: t.Type[logging.FileHandler]):
        for logger_ in [logger, compact_logger]:
            formatter = logger_.handlers[0].formatter if logger_.handlers else logging.Formatter()
            handler = dtype(path)
            handler.setFormatter(formatter)
            logger_.addHandler(handler)

    def remove_log_handler(self, dtype):
        for logger_ in [logger, compact_logger]:
            for handler in logger_.handlers:
                if isinstance(handler, dtype):
                    logger_.removeHandler(handler)
