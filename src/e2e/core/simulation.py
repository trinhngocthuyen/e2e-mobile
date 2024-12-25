import typing as t

from cicd.core.mixin.logger import LoggerMixin

from e2e._typing import WD

S = t.TypeVar('S', bound='Simulation')


class Simulation(LoggerMixin):
    '''Base class for simulations. A simulation is meant for test arrangement.
    For example, sending an API request to prepare resources, or triggering a
    push notification, etc.

    The recommended way to use a simulation is with the `with` statement.
    This way, the cleanup of a simulation (if implemented in the __exit__ method)
    will be triggered.

    .. code-block:: python

        with simulation:
            perform_assertions()
    '''

    def __init__(self, wd: WD) -> None:
        self.wd = wd
        self.kwargs = {}

    def run(self, **kwargs):
        '''Running a simulation. Subclasses need to implement this.'''

    def __call__(self: S, **kwargs) -> S:
        self.kwargs = kwargs
        return self

    def __enter__(self: S) -> S:
        self.logger.info(f'Running simulation: {self.__class__.__name__}, kwargs = {self.kwargs}')
        self.run(**self.kwargs)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.logger.info(f'-> Exit simulation: {self.__class__.__name__}')
