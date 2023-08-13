import importlib.resources
import shutil

from e2e.core.logger import logger


class Template:
    def __init__(self, name: str) -> None:
        self.name = name
        self.templates_dir = importlib.resources.path('e2e', '_templates')

    def unpack(self):
        logger.info(f'Generate `{self.name}` dir from templates')
        for path in self.templates_dir.glob(f'{self.name}/**/*.template'):
            dst_path = path.relative_to(self.templates_dir).with_suffix('')
            if not dst_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, dst_path)
