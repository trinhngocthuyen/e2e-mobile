import shutil
from collections import defaultdict

import pytest

from e2e.core.config import E2EConfig
from e2e.core.env import env
from e2e.core.logger import logger

from .base import Plugin


@pytest.fixture(scope='session', autouse=True)
def e2e_config(request):
    '''E2E config including Appium server URL, artifacts dir, etc..'''
    return E2EConfig.from_pytest_config(request.config)


@pytest.fixture(scope='session', autouse=True)
def e2e_hook_fixture_session():
    '''A special fixture for fixtures cache in e2e-mobile. Do NOT override it.'''
    return 'session'


@pytest.fixture(scope='function', autouse=True)
def e2e_hook_fixture_function():
    '''A special fixture for fixtures cache in e2e-mobile. Do NOT override it.'''
    return 'function'


class CorePlugin(Plugin):
    hook_fixtures = {
        e2e_hook_fixture_session.__name__: [],
        e2e_hook_fixture_function.__name__: ['caplog', 'capsys'],
    }

    @classmethod
    def load_order(cls):
        return 1e9

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        self._cache.set('item', item)
        self.clean_artifacts_dir()
        yield
        delattr(self._cache, 'item')
        if self.wd:
            self.wd.quit()  # Quit driver to release Appium resources
        self.destroy_cached_fixtures(scope='function')

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_fixture_setup(self, fixturedef, request):
        def track_fixure(name, scope):
            if not self._cache._fixtures:
                self._cache._fixtures = defaultdict(set)
            self._cache._fixtures[scope].add(name)

        def load_hook_fixtures():
            for name in self.hook_fixtures.get(fixturedef.argname, []):
                try:
                    self._cache.set(name, request.getfixturevalue(name))
                    track_fixure(name, outcome._result)
                except Exception as e:
                    logger.error(f'Cannot load fixture {name}. Error: {e}')

        outcome = yield
        self._cache.set(fixturedef.argname, outcome._result)
        track_fixure(fixturedef.argname, fixturedef.scope)
        load_hook_fixtures()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_setup(self, item):
        yield

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionstart(self, session):
        yield

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_sessionfinish(self, session, exitstatus):
        if self.is_non_exec_session(session):
            yield
            return
        yield
        self.destroy_cached_fixtures(scope='session')

    @pytest.hookimpl(tryfirst=True)
    def pytest_configure(self, config):
        env._platform = config.option.platform
        self._cache.set('pytest_config', config)
        self._cache.set('e2e_config', E2EConfig.from_pytest_config(config))

    def destroy_cached_fixtures(self, scope):
        for name in self._cache._fixtures[scope]:
            delattr(self._cache, name)
        self._cache._fixtures[scope].clear()

    def clean_artifacts_dir(self):
        if self.artifacts_dir.exists():
            shutil.rmtree(self.artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
