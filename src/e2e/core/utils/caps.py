import typing as t


class Caps:
    def __init__(self, raw: t.Dict[str, t.Any]) -> None:
        self.raw = raw

    def value(self, key: str) -> str | None:
        key = key.removeprefix('appium:')
        return self.raw.get(key) or self.raw.get(f'appium:{key}')

    @property
    def device(self) -> str | None:
        return self.value('deviceName') or self.value('udid')

    @property
    def app_id(self) -> str | None:
        return self.value('bundleId') or self.value('appPackage')
