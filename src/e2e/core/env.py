import os
import typing as t
from enum import Enum

T = t.TypeVar('T')


class Platform(Enum):
    IOS = 'ios'
    ADR = 'android'


class Env:
    def get(
        self,
        key: str,
        default: T | None = None,
        dtype: t.Type[T] | None = None,
    ) -> T | str:
        value = os.getenv(key, default=default)
        return dtype(value) if dtype and value is not None else value

    @property
    def platform(self) -> Platform:
        if hasattr(self, '_platform') and self._platform:
            return Platform(self._platform)
        return Platform(self.get('PLATFORM', default='ios'))

    @property
    def is_ios(self) -> bool:
        return self.platform == Platform.IOS

    @property
    def is_android(self) -> bool:
        return self.platform == Platform.ADR


env = Env()
