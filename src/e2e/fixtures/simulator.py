import typing as t

import pytest
from cicd.ios.simulator import Simulator

from e2e.core.logger import logger

# TODO: Consider moving simulator to a separate pypi package


@pytest.fixture
def prepare_simulator(merged_capabilities: t.Dict[str, t.Any]):
    keys = ['udid', 'appium:udid', 'deviceName', 'appium:deviceName']
    device = next(
        (merged_capabilities[k] for k in keys if k in merged_capabilities), None
    )
    if not device:
        with Simulator(name='E2E') as simulator:
            device = simulator.name
    logger.debug(f'Using device: {device}')
