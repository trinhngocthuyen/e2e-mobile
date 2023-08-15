from e2e.core.logger import logger


class LoggerMixin:
    '''A mixin to easily access the logger.'''

    @property
    def logger(self):
        return logger
