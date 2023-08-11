import pytest

pytest_plugins = [
    'e2e.fixtures.tester',
]


@pytest.fixture
def capabilities():
    return {
        'appium:app': 'tmp/apps/Wikipedia.app',
    }
