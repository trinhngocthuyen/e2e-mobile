import click

from .template import Template


@click.command
@click.option('--dir', help='Dir to extract the templates')
@click.option('--tests/--no-tests', help='Whether to generate example tests', default=True)
def main(**kwargs):
    '''Init the e2e project.'''
    dir = kwargs.get('dir')
    Template('e2e_ext', **kwargs).unpack(dir=dir)
    if kwargs.get('tests'):
        Template('tests', **kwargs).unpack(dir=dir)


if __name__ == '__main__':
    main()
