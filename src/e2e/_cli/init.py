import click

from .template import Template


@click.command
def main():
    '''Init the e2e project.'''
    Template('e2e_ext').unpack()
    Template('tests').unpack()


if __name__ == '__main__':
    main()
