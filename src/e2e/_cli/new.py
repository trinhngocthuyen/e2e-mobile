import click

from e2e._typing import Path
from e2e.core.logger import logger

from .template import Template


@click.group()
def main():
    '''Generate new resources (Screens or Simulations).'''


def update_typing(path: Path, name: str, category: str, cls_name: str):
    logger.info(f'Update typing in {path}')
    content = path.read_text()
    lines = content.splitlines()

    def insert_import_statement():
        import_line = f'from .{category}s.{name} import {cls_name}'
        if import_line not in content:
            lines.insert(0, import_line)

    def insert_annotation():
        annotation_line = f'    {name}: {cls_name}'
        if annotation_line not in content:
            cls_def_line = f'class {category.title()}sTyping'
            idx = next(i for i, line in enumerate(lines) if line.startswith(cls_def_line))
            lines.insert(idx + 1, annotation_line)

    insert_import_statement()
    insert_annotation()
    path.write_text('\n'.join(lines) + '\n')


def gen_resource_and_update_typing(category: str, **kwargs):
    name = kwargs.pop('name')
    dir = Path(kwargs.get('dir') or 'e2e_ext')
    cls_prefix = name.title().replace('_', '')
    cls_name = f'{cls_prefix}{category.title()}'
    generated_path = dir / f'{category}s' / f'{name}.py'
    typing_path = dir / '_typing.py'

    if not typing_path.exists():
        from .init import main as init

        init.callback(**kwargs)

    logger.info(f'Generate class `{cls_name}` to file: {generated_path}')
    template = Template('new', root_templates_pkg=kwargs.get('root_templates_pkg'))
    template.copy_resource(
        path=template.templates_dir / f'{category}.py.template',
        to_path=generated_path,
        template_data={'prefix': cls_prefix},
    )
    update_typing(
        path=typing_path,
        name=name,
        category=category,
        cls_name=cls_name,
    )


@main.command
@click.argument('name')
@click.option('--dir', help='Dir to extract the templates')
@click.option('--root-templates-pkg', help='Root templates pkg')
def screen(**kwargs):
    gen_resource_and_update_typing(category='screen', **kwargs)


@main.command
@click.argument('name')
@click.option('--dir', help='Dir to extract the templates')
@click.option('--root-templates-pkg', help='Root templates pkg')
def simulation(**kwargs):
    gen_resource_and_update_typing(category='simulation', **kwargs)


if __name__ == '__main__':
    main()
