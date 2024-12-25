import typing as t

import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_connection import AppiumConnection
from selenium.webdriver.remote.client_config import ClientConfig

from e2e._typing import WD
from e2e.core.env import Platform, env
from e2e.core.logger import logger
from e2e.core.utils import AppUtils, Caps


@pytest.fixture
def wd(
    e2e_config,
    prepare_simulator,
    merged_capabilities,
    setup_wd,
    setup_wd_options,
):
    '''The web driver used for testing.'''
    if env.platform == Platform.IOS:
        options = XCUITestOptions()
    elif env.platform == Platform.ADR:
        options = UiAutomator2Options()

    options.load_capabilities(merged_capabilities)
    setup_wd_options(options)
    client_config = ClientConfig(e2e_config.appium.server_url)
    connection = AppiumConnection(client_config=client_config)

    logger.debug(f'Create driver: {e2e_config.appium.server_url}. Capabilities: {merged_capabilities}')
    try:
        this = WD(connection, options=options)
    except Exception as e:
        logger.error(f'Cannot create driver. Error: {e}')
        raise e
    setup_wd(this)
    yield this


@pytest.fixture
def setup_wd():
    '''Override this fixture to provide customization for web driver.'''

    def setup(wd: WD):
        pass

    return setup


@pytest.fixture
def setup_wd_options():
    '''Override this fixture to provide customization for Appium options (XCUITestOptions | UiAutomator2Options).'''

    def setup(options: XCUITestOptions | UiAutomator2Options):
        pass

    return setup


@pytest.fixture
def merged_capabilities(
    capabilities: t.Dict[str, t.Any],
):
    '''The final capabilities to be passed to web driver, including some pre-filled ones.'''
    default = {}
    caps = Caps(capabilities)
    app_path = caps.value('app')
    app_id = caps.app_id or AppUtils.get_app_id(app_path=app_path)
    if not app_id:
        logger.warning(
            f'App id was not set in capabilities (`bundleId` in iOS, `appPackage` in Android). '
            'This might lead to some unexpected behaviors. '
            'It is recommended to explicitly set this value. For example: '
            f"{{'bundleId': 'com.example.app'}}"
        )
    return {**default, **capabilities}


@pytest.fixture
def capabilities():
    '''Override this fixture to provide Appium capabilities for testing.
    Refer to these docs for the extensive list of capabilities:
    - iOS: https://github.com/appium/appium-xcuitest-driver/blob/master/docs/reference/capabilities.md
    - Android: https://github.com/appium/appium-uiautomator2-driver/tree/master#capabilities
    '''
    return {}
