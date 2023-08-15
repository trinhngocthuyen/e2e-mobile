import time
import typing as t
from functools import cached_property

from e2e._typing import WD
from e2e.core.mixin.logger import LoggerMixin


class WDMixin(LoggerMixin):
    wd: WD

    def wait(self, seconds: float = 1):
        self.logger.debug(f'Wait for {seconds}s')
        time.sleep(seconds)

    @cached_property
    def window_size(self) -> t.Tuple[float, float]:
        size = self.wd.get_window_size()
        return (size['width'], size['height'])

    @property
    def app_id(self) -> t.Optional[str]:
        if value := self.wd.capabilities.get('bundleId'):
            return value
        if value := self.wd.capabilities.get('appPackage'):
            return value

    def relaunch_app(self, app_id: t.Optional[str] = None):
        app_id = app_id or self.app_id
        self.logger.info(f'Relaunch the app: {app_id}')
        if not app_id:
            self.logger.warning('Cannot detect app_id for app relaunch')
        self.wd.terminate_app(app_id=app_id)
        self.wd.activate_app(app_id=app_id)

    def swipe(
        self,
        direction: str = 'up',
        xy_ratio_start: t.Optional[t.Tuple[float, float]] = None,
        xy_ratio_end: t.Optional[t.Tuple[float, float]] = None,
        duration: float = 0,
    ):
        w, h = self.window_size
        ratio_small, ratio_big = 0.2, 0.8
        start, end = {
            'up': ((w * 0.5, h * ratio_big), (w * 0.5, h * ratio_small)),
            'down': ((w * 0.5, h * ratio_small), (w * 0.5, h * ratio_big)),
            'left': ((w * ratio_big, h * 0.5), (w * ratio_small, h * 0.5)),
            'right': ((w * ratio_small, h * 0.5), (w * ratio_big, h * 0.5)),
        }.get(direction)
        if xy_ratio_start:
            start = (w * xy_ratio_start[0], h * xy_ratio_start[1])
        if xy_ratio_end:
            end = (w * xy_ratio_end[0], h * xy_ratio_end[1])
        self.logger.debug(f'Swipe {direction}: {start = }, {end = }')
        self.wd.swipe(
            start_x=int(start[0]),
            start_y=int(start[1]),
            end_x=int(end[0]),
            end_y=int(end[1]),
            duration=int(duration * 1000),
        )
