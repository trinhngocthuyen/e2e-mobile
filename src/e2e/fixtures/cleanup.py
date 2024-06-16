import pytest
from cicd.core.logger import logger
from cicd.core.utils.sh import sh


@pytest.fixture(scope='session', autouse=True)
def cleanup_config():
    return {'cleanup_ports': True}


@pytest.fixture(scope='session', autouse=True)
def cleanup(request, cleanup_config, ports_config):
    def cleanup_ports():
        # Don't close Appium port, Appium stops in `appium_service` fixture
        excluded = {'appium'}
        to_close = [v for k, v in ports_config.items() if k not in excluded]
        for port in to_close:
            logger.info(f'Closing port: {port}...')
            sh.exec(f'kill $(lsof -t -i:{port}) || true')

    if cleanup_config.get('cleanup_ports'):
        request.addfinalizer(cleanup_ports)
