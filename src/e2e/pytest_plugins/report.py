import os
from functools import cached_property
from pathlib import Path

import pytest
from pytest_html import extras

from .base import Plugin


class ReportPlugin(Plugin):
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        self.attach_links_to_report(report)

    @cached_property
    def html_path(self):
        path = self.pytest_config.option.htmlpath
        return Path(path) if path else None

    def attach_links_to_report(self, report):
        if report.outcome == 'passed' and report.when != 'call':
            return
        if not self.html_path or not self.wd:
            return

        def add_link(path: Path):
            relpath = os.path.relpath(path.absolute(), self.html_path.parent.absolute())
            report.extras.append(extras.url(relpath, name=path.name))

        if not hasattr(report, 'extras'):
            report.extras = []
        add_link(self.artifacts_dir / 'screenshot.png')
        add_link(self.artifacts_dir / 'recording.mp4')
        add_link(self.artifacts_dir / 'page_source.xml')
