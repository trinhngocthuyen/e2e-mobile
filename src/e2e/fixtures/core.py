import typing as t

import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from cicd.core.logger import logger

from e2e._typing import WD
from e2e.core.env import Platform, env
from e2e.core.utils import AppUtils, WDUtils


@pytest.fixture
def wd(
    appium_config,
    appium_service,
    prepare_simulator,
    merged_capabilities,
    setup_wd,
    setup_wd_options,
) -> WD:
    if env.platform == Platform.IOS:
        options = XCUITestOptions()
    elif env.platform == Platform.ADR:
        options = UiAutomator2Options()
    logger.debug(f'Capabilities: {merged_capabilities}')
    options.load_capabilities(merged_capabilities)
    setup_wd_options(options)
    host, port = appium_config.get('host'), appium_config.get('port')
    this = WD(f'http://{host}:{port}', options=options)
    setup_wd(this)
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
def setup_wd():
    def setup(wd: WD):
        pass

    return setup


@pytest.fixture
def setup_wd_options():
    def setup(options: XCUITestOptions | UiAutomator2Options):
        pass

    return setup


@pytest.fixture
def merged_capabilities(capabilities: t.Dict[str, t.Any]):
    default = {}
    app_path = capabilities.get('app') or capabilities.get('appium:app')
    if not capabilities.get('bundleId') and not capabilities.get('appPackage'):
        key = {
            Platform.IOS: 'bundleId',
            Platform.ADR: 'appPackage',
        }.get(env.platform)
        if app_id := AppUtils.get_app_id(app_path=app_path):
            capabilities[key] = app_id
        else:
            logger.warning(
                f'The key `{key}` was not set in capabilities. '
                'This might lead to some unexpected behaviors. '
                'It is recommended to explicitly set this value. For example: '
                f"{{'{key}': 'com.example.app'}}"
            )
    return {**default, **capabilities}


@pytest.fixture
def capabilities():
    return {}


@pytest.fixture(scope='session')
def appium_service(appium_config, session_artifacts_dir):
    logger.info('Starting Appium...')
    service = AppiumService()
    appium_log_path = session_artifacts_dir / 'appium.log'
    with appium_log_path.open('wb') as f:
        service.start(
            args=[
                '--address',
                appium_config.get('host'),
                '-p',
                str(appium_config.get('port')),
            ],
            stdout=f,
            stderr=f,
            timeout_ms=20000,
        )
    yield service
    service.stop()
    logger.info('Stopping Appium...')
