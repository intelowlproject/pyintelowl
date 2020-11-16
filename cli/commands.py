import click
from ._utils import ClickContext
from rich import print


@click.command(
    short_help="Get current state of `analyzer_config.json` from the IntelOwl instance"
)
@click.pass_context
def get_analyzer_config(ctx: ClickContext):
    res, err = ctx.obj.get_analyzer_configs()
    if err:
        print(err)
    else:
        print(res)
