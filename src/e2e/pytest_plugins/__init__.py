from pathlib import Path

from e2e.core.utils import MetaUtils

from .appium_service import *
from .base import *
from .core import *
from .diagnostics import *
from .log import *
from .parallel import *
from .simulator import *
from .tester import *
from .wd import *


def pytest_configure(config):
    for cls in sorted(MetaUtils.all_subclasses(Plugin), key=lambda x: x.load_order()):
        config.pluginmanager.register(cls(), name=cls.__module__)


def pytest_addoption(parser: pytest.Parser, pluginmanager):
    group = parser.getgroup('e2e-mobile')
    group.addoption('--artifacts', type=Path, help='Artifacts dir')
    group.addoption(
        '--appium', default='http://127.0.0.1:4723', help='Appium server URL'
    )
