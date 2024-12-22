import pytest

from e2e.core.config import E2EConfig
from e2e.tester import Tester


@pytest.fixture
def tester(
    request,
    e2e_config: E2EConfig,
    wd,
):
    '''Use this fixture in your tests to perform test actions or simulations.
    Example:

        def test_example(tester: Tester):
            tester.ui.element('Settings').tap()
            ...
    '''
    return Tester(wd=wd, artifacts_dir=e2e_config.artifacts_dir_of(request.node.name))
