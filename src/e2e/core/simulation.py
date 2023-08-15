import typing as t

from e2e.core.mixin.logger import LoggerMixin

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

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def run(self, *args, **kwargs):
        '''Running a simulation. Subclasses need to implement this.'''

    def __call__(self: S, *args, **kwargs) -> S:
        self.args = args
        self.kwargs = kwargs
        return self

    def __enter__(self):
        self.logger.info(
            f'Running simulation: {self.__class__.__name__}, '
            f'args = {self.args}, kwargs = {self.kwargs}'
        )
        self.run(*self.args, **self.kwargs)

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.logger.info(f'-> Exit simulation: {self.__class__.__name__}')
