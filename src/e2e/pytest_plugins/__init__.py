# from .artifacts import *
# from .base import *
# from .cleanup import *
# from .core import *
# from .diagnostic import *
# from .parallel import *
# from .simulator import *
# from .tester import *
# from .log import *

pytest_plugins = [
    'e2e.pytest_plugins.base',
    'e2e.pytest_plugins.core',
    'e2e.pytest_plugins.artifacts',
    'e2e.pytest_plugins.cleanup',
    'e2e.pytest_plugins.diagnostic',
    'e2e.pytest_plugins.parallel',
    'e2e.pytest_plugins.simulator',
    'e2e.pytest_plugins.tester',
    'e2e.pytest_plugins.log',
]
