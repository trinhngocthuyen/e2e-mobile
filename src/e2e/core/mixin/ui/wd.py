import time
import typing as t
from functools import cached_property

from e2e._typing import WD
from e2e.core.mixin.logger import LoggerMixin

__all__ = ['WDMixin']

Coordinate = t.Tuple[float, float]
CoordinateRatio = t.Tuple[float, float]
Area = t.Literal[
    'center',
    'top',
    'bottom',
    'left',
    'right',
    'top_left',
    'top_right',
    'bottom_left',
    'bottom_right',
]


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
        xy_ratio_start: t.Optional[CoordinateRatio] = None,
        xy_ratio_end: t.Optional[CoordinateRatio] = None,
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

    def tap_coordinates(
        self,
        xy: t.Union[t.List[Coordinate], Coordinate, None] = None,
        xy_ratios: t.Union[t.List[CoordinateRatio], CoordinateRatio, None] = None,
        duration: t.Optional[float] = None,
    ):
        positions = []
        if isinstance(xy, tuple):
            xy = [xy]
        if isinstance(xy_ratios, tuple):
            xy_ratios = [xy_ratios]
        if xy:
            positions = [(int(x), int(y)) for x, y in xy]
        elif xy_ratios:
            w, h = self.window_size
            positions = [(int(xr * w), int(yr * h)) for xr, yr in xy_ratios]
        else:
            raise ValueError('xy and xy_ratios cannot be both None')
        duration_in_ms = int(duration * 1000) if duration else None
        self.wd.tap(positions=positions, duration=duration_in_ms)

    def tap_area(self, area: Area):
        xy_ratio = {
            'center': (0.5, 0.5),
            'top': (0.5, 0.2),
            'bottom': (0.5, 0.8),
            'left': (0.2, 0.5),
            'right': (0.8, 0.5),
            'top_left': (0.2, 0.2),
            'top_right': (0.8, 0.2),
            'bottom_left': (0.2, 0.8),
            'bottom_right': (0.8, 0.8),
        }.get(area)
        self.tap_coordinates(xy_ratios=xy_ratio)
