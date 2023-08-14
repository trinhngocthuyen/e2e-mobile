import shutil
import subprocess
from pathlib import Path

import click

from e2e.core.logger import logger

__all__ = ['main']


class Demo:
    def __init__(self) -> None:
        self.tmp_dir = Path('/tmp/wikipedia-ios')
        self.repo_url = 'https://github.com/wikimedia/wikipedia-ios.git'

    def build(self):
        self.clone_project()
        self.xcodebuild()
        self.copy_app_bundle()

    def exec(self, cmd, **kwargs):
        logger.debug(f'$ {cmd}')
        subprocess.run(cmd, shell=True, check=True, **kwargs)

    def clone_project(self):
        if not self.tmp_dir.exists():
            self.exec(
                f'git clone --depth=1 --single-branch {self.repo_url} {self.tmp_dir}'
            )

    def xcodebuild(self):
        logger.info('Building the project. This might take a while...')
        cd_cmd = f'cd {self.tmp_dir}'
        xcodebuild_cmd = (
            'set -o pipefail && xcodebuild build -derivedDataPath DerivedData '
            '-scheme Wikipedia -destination "generic/platform=iOS Simulator"'
        )
        if shutil.which('xcbeautify'):
            xcodebuild_cmd += ' | xcbeautify'
        elif shutil.which('xcpretty'):
            xcodebuild_cmd += ' | xcpretty'
        self.exec(f'{cd_cmd} && {xcodebuild_cmd}')

    def copy_app_bundle(self):
        src_path = (
            self.tmp_dir
            / 'DerivedData'
            / 'Build'
            / 'Products'
            / 'Debug-iphonesimulator'
            / 'Wikipedia.app'
        )
        dst_path = Path('tmp/apps/example.app')
        logger.info(f'Copy app bundle from {src_path} to {dst_path}')
        if dst_path.exists():
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)


@click.group()
def main():
    '''CLI to work with the demo.'''


@main.command
def build():
    Demo().build()


if __name__ == '__main__':
    main()
