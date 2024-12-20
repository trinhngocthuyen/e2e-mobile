import typing as t

import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_connection import AppiumConnection
from appium.webdriver.appium_service import AppiumService
from selenium.webdriver.remote.client_config import ClientConfig

from cicd.core.logger import logger

from e2e._typing import WD
from e2e.core.env import Platform, env
from e2e.core.utils import AppUtils, Caps, WDUtils


@pytest.fixture
def wd(
    appium_config,
    appium_service,
    prepare_simulator,
    merged_capabilities,
    setup_wd,
    setup_wd_options,
) -> WD:  # type: ignore
    if env.platform == Platform.IOS:
        options = XCUITestOptions()
    elif env.platform == Platform.ADR:
        options = UiAutomator2Options()
    logger.debug(f'Capabilities: {merged_capabilities}')
    options.load_capabilities(merged_capabilities)
    setup_wd_options(options)
    host, port = appium_config.get('host'), appium_config.get('port')

    client_config = ClientConfig(f'http://{host}:{port}')
    connection = AppiumConnection(client_config=client_config)
    this = WD(connection, options=options)
    setup_wd(this)
    yield this
    this.quit()


@pytest.fixture
def wd_utils(wd):
    return WDUtils(wd=wd)


@pytest.fixture(scope='session')
def ports_config(parallel_worker_id):
    offset = parallel_worker_id or 0
    return {
        'appium': 4723 + offset,
        'wdaLocalPort': 8100 + offset,
        'mjpegServerPort': 9100 + offset,
    }


@pytest.fixture(scope='session')
def appium_config(ports_config):
    return {
        'host': '127.0.0.1',
        'port': ports_config.get('appium'),
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
def merged_capabilities(
    capabilities: t.Dict[str, t.Any],
    ports_config: t.Dict[str, t.Any],
):
    default = {
        'wdaLocalPort': ports_config.get('wdaLocalPort'),
        'mjpegServerPort': ports_config.get('mjpegServerPort'),
    }
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
    return {}


@pytest.fixture(scope='session')
def appium_service(
    appium_config,
    parallel_worker_id,
    session_artifacts_dir,
):
    host, port = appium_config.get('host'), appium_config.get('port')
    logger.info(f'Starting Appium ({host}:{port})..')

    suffix = '' if parallel_worker_id is None else f'_{parallel_worker_id + 1}'
    appium_log_path = session_artifacts_dir / f'appium{suffix}.log'
    service = AppiumService()
    with appium_log_path.open('wb') as f:
        service.start(
            args=[
                '--address',
                host,
                '-p',
                str(port),
            ],
            stdout=f,
            stderr=f,
            timeout_ms=20000,
        )
    yield service
    service.stop()
    logger.info('Stopping Appium...')
