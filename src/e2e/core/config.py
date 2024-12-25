from pathlib import Path

from e2e.core.appium.config import AppiumConfig


class E2EConfig:
    def __init__(self, **kwargs):
        self.appium = AppiumConfig(server_url=kwargs.get('appium'))
        self.session_artifacts_dir: Path = kwargs.get('session_artifacts_dir', '.artifacts')
        self.session_artifacts_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def from_pytest_config(config):
        return E2EConfig(
            appium=config.option.appium,
            session_artifacts_dir=config.option.artifacts,
        )

    def artifacts_dir_of(self, node_name: str):
        path = self.session_artifacts_dir / node_name
        path.mkdir(parents=True, exist_ok=True)
        return path
