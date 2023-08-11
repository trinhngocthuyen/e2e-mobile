import typing as t
from pathlib import Path

from appium.webdriver.webdriver import WebDriver

StrPath = t.Union[str, Path]
WD = WebDriver
