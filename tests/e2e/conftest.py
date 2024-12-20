import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from e2e._typing import WD

pytest_plugins = [
    'e2e.pytest_plugins',
]


@pytest.fixture
def setup_wd():
    def setup(wd: WD):
        # Provide additional setup to WD
        pass

    return setup


@pytest.fixture
def setup_wd_options():
    def setup(options: XCUITestOptions | UiAutomator2Options):
        # Provide additional setup to WD options (XCUITestOptions/UiAutomator2Options)
        pass

    return setup


@pytest.fixture
def capabilities():
    return {
        'appium:app': 'tmp/apps/Wikipedia.zip',  # TODO: Update the path to the app here
        'appium:bundleId': 'org.wikimedia.wikipedia',
    }
