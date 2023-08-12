from e2e.core.logger import logger


class LoggerMixin:
    @property
    def logger(self):
        return logger
