import click

from e2e._cli.init import main as init
from e2e._cli.new import main as new


@click.group()
def main():
    pass


main.add_command(init, name='init')
main.add_command(new, name='new')


if __name__ == '__main__':
    main()
