import types
import typing as t
from pathlib import Path

from e2e._typing import StrPath
from e2e.core.utils import ModuleUtils

D = t.TypeVar('D')


class DynamicAttrsMixin:
    def _load_source(self, dir: StrPath) -> t.Dict[str, types.ModuleType]:
        results = {}
        for path in Path(dir).glob('**/*.py'):
            if path.stem == '__init__':
                continue
            module_name = str(path.with_suffix('')).replace('/', '.')
            results[module_name] = ModuleUtils.load_source(
                path=path, module_name=module_name
            )
        return results

    def set_dynamic_attrs(
        self,
        cls: t.Type[D],
        attr_kwargs: t.Optional[t.Dict[str, t.Any]] = None,
        load_source_in_dir: t.Optional[str] = None,
    ):
        if load_source_in_dir:
            self._load_source(load_source_in_dir)
        if not attr_kwargs:
            attr_kwargs = {}
        for subclass in cls.__subclasses__():
            attr_name = subclass.__module__.split('.')[-1]
            attr = subclass(**attr_kwargs)
            setattr(self, attr_name, attr)
