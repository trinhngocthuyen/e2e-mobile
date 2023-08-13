import click


@click.group()
def main():
    '''Generate new resources (Screens or Simulations).'''


@main.command
@click.argument('name')
def screen(**kwargs):
    pass


@main.command
@click.argument('name')
def simulation(**kwargs):
    pass


if __name__ == '__main__':
    main()
