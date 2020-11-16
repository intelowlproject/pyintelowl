import click

from ._utils import ClickContext


@click.group("config", invoke_without_command=True)
@click.pass_context
def config(ctx: ClickContext):
    """
    Set or view config variables
    """
    pass
