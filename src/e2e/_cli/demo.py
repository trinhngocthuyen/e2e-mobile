import os
import shutil
from pathlib import Path

import click

from cicd.core.utils.file import FileUtils
from cicd.core.utils.sh import sh
from cicd.ios.mixin.build import BuildMixin

from e2e.core.logger import logger

__all__ = ['main']


class Demo:
    def __init__(self) -> None:
        self.tmp_dir = Path('/tmp/wikipedia-ios')
        self.repo_url = 'https://github.com/wikimedia/wikipedia-ios.git'
        self.dst_path = Path('tmp/apps/Wikipedia.zip')
        self.dst_path.parent.mkdir(parents=True, exist_ok=True)

    def build(self, prebuilt=False, **kwargs):
        if prebuilt:
            cmd = f'curl https://raw.githubusercontent.com/trinhngocthuyen/prebuilt/main/wikipedia/Wikipedia.zip -o {self.dst_path}'
            sh.exec(cmd, log_cmd=True, capture_output=False)
            return
        self.clone_project()
        self.xcodebuild()
        self.copy_app_bundle()

    def clone_project(self):
        if not self.tmp_dir.exists():
            cmd = f'git clone --depth=1 --single-branch {self.repo_url} {self.tmp_dir}'
            sh.exec(cmd, capture_output=False, log_cmd=True)

    def xcodebuild(self):
        logger.info('Building the project. This might take a while...')
        logger.debug('Using Xcode: {}'.format(sh.exec('xcode-select -p')))
        workdir = Path().absolute()
        os.chdir(self.tmp_dir)
        try:
            BuildMixin(
                scheme='Wikipedia',
                destination='generic/platform=iOS Simulator',
                derived_data_path='DerivedData',
            ).start_building()
        finally:
            os.chdir(workdir)

    def copy_app_bundle(self):
        build_dir = self.tmp_dir / 'DerivedData' / 'Build' / 'Products' / 'Debug-iphonesimulator'
        if self.dst_path.exists():
            shutil.rmtree(self.dst_path)
        sh.exec(f'cd "{build_dir.absolute()}" && zip -r Wikipedia.zip Wikipedia.app')
        FileUtils.copy(build_dir / 'Wikipedia.zip', self.dst_path)


@click.group()
def main():
    '''CLI to work with the demo.'''


@main.command
@click.option('--prebuilt', is_flag=True)
def build(**kwargs):
    Demo().build(**kwargs)


if __name__ == '__main__':
    main()
