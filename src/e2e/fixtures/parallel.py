import re
import typing as t

import pytest


@pytest.fixture(scope='session')
def parallel_config(parallel_worker_id) -> t.Dict[str, t.Any]:
    if parallel_worker_id is None:
        return {}
    return {'parallel_worker_id': parallel_worker_id}


@pytest.fixture(scope='session')
def parallel_worker_id(worker_id):
    if m := re.match(r'\D*(\d+)', worker_id):
        return int(m.group(1))
