import types
from importlib import machinery
from pathlib import Path

from e2e._typing import StrPath


class ModuleUtils:
    @staticmethod
    def load_source(path: StrPath, module_name: str | None = None) -> types.ModuleType:
        if not module_name:
            module_name = Path(path).stem
        loader = machinery.SourceFileLoader(module_name, str(path))
        module = types.ModuleType(loader.name)
        loader.exec_module(module)
        return module
