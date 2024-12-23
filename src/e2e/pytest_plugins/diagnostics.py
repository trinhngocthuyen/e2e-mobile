import pytest

from e2e.core.utils import failable

from .base import Plugin


class DiagnosticsPlugin(Plugin):
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_setup(self, item):
        yield
        self.start_recording()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        yield
        self.stop_recording()
        self.save_screenshot()
        self.save_page_source()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        yield

    @failable()
    def start_recording(self):
        if self.wd_utils:
            self.wd_utils.start_recording()

    @failable()
    def stop_recording(self):
        if self.wd_utils:
            self.wd_utils.stop_recording(self.artifacts_dir / 'recording.mp4')

    @failable()
    def save_screenshot(self):
        if self.wd_utils:
            self.wd_utils.take_screenshot(self.artifacts_dir / 'screenshot.png')

    @failable()
    def save_page_source(self):
        if self.wd_utils:
            self.wd_utils.save_page_source(self.artifacts_dir / 'page_source.xml')
