import time
import typing as t
from functools import cached_property

from cicd.core.mixin.logger import LoggerMixin

from e2e._typing import WD
from e2e.core.env import env
from e2e.core.utils.wd import WDUtils

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
    def app_id(self) -> str | None:
        return WDUtils.app_id_from_caps(self.wd.capabilities)

    def terminate_app(self, app_id: str | None = None):
        self.logger.info(f'Terminate app: {app_id}')
        self.wd.terminate_app(app_id or self.app_id)

    def relaunch_app(self, app_id: str | None = None, **kwargs):
        app_id = app_id or self.app_id
        if not app_id:
            self.logger.warning('Cannot detect app_id for app relaunch')
        self.terminate_app(app_id=app_id)
        if kwargs:  # Possibly launch with environment/intent argument
            self.launch_app_with_env(app_id=app_id, **kwargs)
        else:
            self.activate_app(app_id)

    def activate_app(self, app_id: str):
        self.logger.info(f'Activate app: {app_id}')
        self.wd.activate_app(app_id=app_id)

    def launch_app_with_env(self, app_id: str, **kwargs):
        '''Launch app with environment. iOS uses `environment`, Android uses `extras`.

        Refer to these docs for the environment params.
        - iOS: https://appium.github.io/appium-xcuitest-driver/latest/reference/execute-methods#mobile-launchapp
        - Android: https://github.com/appium/appium-uiautomator2-driver/tree/master#mobile-startactivity
        '''
        self.logger.info(f'Launch app: {app_id}, {kwargs = }')
        if env.is_ios:
            return self.execute_script('mobile: launchApp', {'bundleId': app_id, **kwargs})
        return self.execute_script('mobile: startActivity', {'intent': app_id, **kwargs})

    def execute_script(self, script: str, *args):
        # https://github.com/appium/appium-xcuitest-driver/blob/master/lib/execute-method-map.ts
        return self.wd.execute_script(script, *args)

    def swipe(
        self,
        direction: str = 'up',
        xy_ratio_start: CoordinateRatio | None = None,
        xy_ratio_end: CoordinateRatio | None = None,
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
        xy: t.List[Coordinate] | Coordinate | None = None,
        xy_ratios: t.List[CoordinateRatio] | CoordinateRatio | None = None,
        duration: float | None = None,
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

    def hide_keyboard(
        self,
        key_name: str | None = None,
        key: str | None = None,
        strategy: str | None = None,
    ):
        self.wd.hide_keyboard(key_name=key_name, key=key, strategy=strategy)
