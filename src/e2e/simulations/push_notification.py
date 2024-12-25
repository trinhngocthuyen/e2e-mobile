import typing as t

from cicd.core.syntax.json import JSON
from cicd.core.utils.file import FileUtils
from cicd.core.utils.sh import sh

from e2e._typing import StrPath
from e2e.core.env import Platform, env
from e2e.core.simulation import Simulation
from e2e.core.utils import WDUtils


class PushNotificationSimulation(Simulation):
    def run(self, **kwargs):
        if env.platform == Platform.IOS:
            self.ios_push_notification(**kwargs)
        else:
            self.logger.warning(f'Push notification is not yet implemented in platform: {env.platform}')

    def ios_push_notification(
        self,
        json_path: StrPath | None = None,
        payload: t.Dict[str, t.Any] | None = None,
    ):
        with FileUtils.tempdir() as dir:
            if not json_path and not payload:
                raise ValueError('json_path and payload cannot be both None')
            if payload:
                json_path = dir / 'notification.json'
                JSON(data=payload).save(json_path)
            device = WDUtils.device_from_caps(self.wd.capabilities)
            app_id = WDUtils.app_id_from_caps(self.wd.capabilities)
            self.logger.debug(f'Push notification: {json_path = }')
            sh.exec(f'xcrun simctl push {device} {app_id} {sh.quote(json_path)}')

    def __call__(
        self,
        payload: t.Dict[str, t.Any] | None = None,
        json_path: StrPath | None = None,
    ) -> 'PushNotificationSimulation':
        return super().__call__(payload=payload, json_path=json_path)
