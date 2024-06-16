import click
import pkg_resources

from e2e._cli.demo import main as demo
from e2e._cli.init import main as init
from e2e._cli.new import main as new


@click.group()
@click.version_option(package_name='e2e-mobile')
def main():
    pass


main.add_command(demo, name='demo')
main.add_command(init, name='init')
main.add_command(new, name='new')

for entry_point in pkg_resources.iter_entry_points('e2e.cli_plugins'):
    main.add_command(entry_point.load(), entry_point.name)

if __name__ == '__main__':
    main()
