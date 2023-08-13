import typing as t

from e2e._typing import WD
from e2e.core.mixin.logger import LoggerMixin


class WDMixin(LoggerMixin):
    wd: WD

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
