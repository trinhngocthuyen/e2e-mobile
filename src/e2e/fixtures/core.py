import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService

from e2e._typing import WD
from e2e.core.env import Platform, env
from e2e.core.logger import logger
from e2e.core.utils import WDUtils


@pytest.fixture
def wd(
    appium_config,
    appium_service,
    default_capabilities,
    update_options,
    capabilities,
) -> WD:
    if env.platform == Platform.IOS:
        options = XCUITestOptions()
    elif env.platform == Platform.ADR:
        options = UiAutomator2Options()
    update_options(options)
    caps = {**default_capabilities, **capabilities}
    logger.debug(f'Capabilities: {caps}')
    options.load_capabilities(caps)
    host, port = appium_config.get('host'), appium_config.get('port')
    this = WD(f'http://{host}:{port}', options=options)
    yield this
    this.quit()


@pytest.fixture
def wd_utils(wd):
    return WDUtils(wd=wd)


@pytest.fixture(scope='session')
def appium_config():
    return {
        'host': '127.0.0.1',
        'port': 4723,
    }


@pytest.fixture
def update_options():
    def fn(options):
        pass

    return fn


@pytest.fixture
def default_capabilities():
    return {'appium:app': None}


@pytest.fixture
def capabilities():
    return {}


@pytest.fixture(scope='session')
def appium_service(appium_config):
    logger.info('Starting Appium...')
    service = AppiumService()
    service.start(
        args=[
            '--address',
            appium_config.get('host'),
            '-p',
            str(appium_config.get('port')),
        ],
        timeout_ms=20000,
    )
    yield service
    service.stop()
    logger.info('Stopping Appium...')
