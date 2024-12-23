import importlib.resources
import shutil
import string
import typing as t

from e2e._typing import Path
from e2e.core.logger import logger


class Template:
    def __init__(self, name: str, **kwargs) -> None:
        root_templates_pkg = kwargs.get('root_templates_pkg') or 'e2e._templates'
        self.name = name
        self.root_templates_dir = importlib.resources.path(root_templates_pkg, '')
        self.templates_dir = self.root_templates_dir / name

    def copy_resource(
        self,
        path: Path,
        to_path: Path | None = None,
        to_dir: Path | None = None,
        template_data: t.Dict[str, str] | None = None,
    ):
        if not to_path and not to_dir:
            raise ValueError('to_path and to_dir cannot be both None')
        if not to_path:
            rel_path = path.relative_to(self.templates_dir)
            to_path = to_dir / rel_path.with_suffix('')
        to_path.parent.mkdir(parents=True, exist_ok=True)
        if not to_path.exists():
            if template_data:
                content = string.Template(path.read_text()).substitute(template_data)
                to_path.write_text(content)
            else:
                shutil.copyfile(path, to_path)

    def unpack(self, dir=None):
        dir = Path(dir or self.name)
        logger.info(f'Generate `{self.name}` dir from templates')
        for path in self.templates_dir.glob('**/*.template'):
            self.copy_resource(path=path, to_dir=dir)
