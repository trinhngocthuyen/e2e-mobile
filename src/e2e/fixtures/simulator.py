import typing as t

import pytest

from cicd.core.logger import logger
from cicd.ios.simulator import Simulator

from e2e.core.utils import WDUtils

# TODO: Consider moving simulator to a separate pypi package


@pytest.fixture
def prepare_simulator(
    merged_capabilities: t.Dict[str, t.Any],
    parallel_worker_id: t.Optional[int],
) -> str:
    device = WDUtils.device_from_caps(merged_capabilities)
    if not device:
        name = 'E2E' if parallel_worker_id is None else f'E2E-{parallel_worker_id + 1}'
        with Simulator(name=name) as simulator:
            device = simulator.name
            merged_capabilities['deviceName'] = device
    logger.debug(f'Using device: {device}')
    return device
