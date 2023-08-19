import typing as t

import pytest
from cicd.core.logger import logger
from cicd.ios.simulator import Simulator

from e2e.core.utils import WDUtils

# TODO: Consider moving simulator to a separate pypi package


@pytest.fixture
def prepare_simulator(merged_capabilities: t.Dict[str, t.Any]):
    device = WDUtils.device_from_caps(merged_capabilities)
    if not device:
        with Simulator(name='E2E') as simulator:
            device = simulator.name
    logger.debug(f'Using device: {device}')
