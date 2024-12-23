from pathlib import Path

import pytest

from e2e._typing import WD
from e2e.core.config import E2EConfig
from e2e.core.utils import WDUtils

__all__ = ['Plugin']


class PluginCache:
    def __getattr__(self, name):
        return None

    def set(self, name, value):
        setattr(self, name, value)


_cache = PluginCache()


class Plugin:
    _cache = _cache

    @classmethod
    def load_order(cls):
        return 0

    @property
    def wd(self) -> WD:
        return self._cache.wd

    @property
    def session_artifacts_dir(self) -> Path:
        return self.e2e_config.session_artifacts_dir

    @property
    def artifacts_dir(self) -> Path:
        if self.item:
            return self.e2e_config.artifacts_dir_of(self.item.name)
        return self.session_artifacts_dir

    @property
    def wd_utils(self) -> WDUtils | None:
        return WDUtils(self.wd) if self.wd else None

    @property
    def pytest_config(self) -> pytest.Config | None:
        return self._cache.pytest_config

    @property
    def item(self) -> pytest.Item | None:
        return self._cache.item

    @property
    def e2e_config(self) -> E2EConfig | None:
        return self._cache.e2e_config

    @property
    def appium_config(self):
        return self.e2e_config.appium

    def is_non_exec_session(self, session):
        return session.config.option.collectonly or session.config.option.showfixtures
