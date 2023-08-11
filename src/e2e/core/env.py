import os
from enum import Enum


class Platform(Enum):
    IOS = 'ios'
    ADR = 'android'


class Env:
    @property
    def platform(self) -> Platform:
        return Platform(os.getenv('PLATFORM', 'ios'))

    @property
    def is_ios(self) -> bool:
        return self.platform == Platform.IOS


env = Env()
