import re

import pytest


@pytest.fixture(scope='session')
def parallel_worker_id(request):
    '''A fixture indicating the parallel worker id (starting from 0) when using pytest-xdist.
    This returns None when pytest-xdist is not being used.
    '''
    try:
        worker_id = request.getfixturevalue('worker_id')
    except:
        return None
    if m := re.match(r'\D*(\d+)', worker_id):
        return int(m.group(1))
