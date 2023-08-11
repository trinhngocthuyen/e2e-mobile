import logging
from enum import Enum

__all__ = ['logger']


class AnsiColorHandler(logging.StreamHandler):
    Color = Enum('Color', 'BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE', start=30)
    CSI = '\033['
    LOGLEVEL_COLORS = {
        'DEBUG': Color.WHITE,
        'INFO': Color.GREEN,
        'WARNING': Color.YELLOW,
        'ERROR': Color.RED,
        'CRITICAL': Color.RED,
    }
    FMT = '[%(levelname)s] %(message)s'

    def __init__(self) -> None:
        super().__init__()
        self.formatter = logging.Formatter(self.FMT)

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if self.stream.isatty() and (
            color := self.LOGLEVEL_COLORS.get(record.levelname)
        ):
            message = f'{self.CSI}{color.value}m{message}{self.CSI}0m'
        return message


def config_logger():
    this = logging.getLogger('e2e')
    this.setLevel(logging.DEBUG)
    this.addHandler(AnsiColorHandler())
    return this


logger = config_logger()
