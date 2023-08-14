import pytest

pytest_plugins = [
    'e2e.fixtures',
]


@pytest.fixture
def capabilities():
    return {
        'app': 'tmp/apps/example.app',
    }
