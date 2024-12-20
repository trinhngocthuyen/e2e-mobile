import pytest


class Plugin:
    def get_fixture(self, item, name: str):
        import pdb

        pdb.set_trace()
        return item.funcargs.get(name)


def pytest_configure(config: pytest.Config):
    for cls in Plugin.__subclasses__():
        print(f'--> [debug] Register plugins: {cls.__name__}')
        config.pluginmanager.register(cls(), cls.__name__)
