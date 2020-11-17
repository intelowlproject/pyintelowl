import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from pyintelowl.exceptions import IntelOwlAPIException

from ._utils import ClickContext


@click.command(short_help="Manage tags")
@click.option("-a", "--all", is_flag=True, help="List all tags")
@click.option("--id", type=int, default=0, help="Retrieve tag details by ID")
@click.pass_context
def tags(ctx: ClickContext, id: int, all: bool):
    """
    Manage tags
    """
    try:
        if all:
            ans = ctx.obj.get_all_tags()
        elif id:
            ans = ctx.obj.get_tag_by_id(id)
            ans = [ans]
        _print_tags_table(ctx, ans)
    except IntelOwlAPIException as e:
        ctx.obj.logger.fatal(str(e))


def _print_tags_table(ctx, rows):
    console = Console()
    table = Table(show_header=True, title="List of tags", box=box.DOUBLE_EDGE)
    for h in ["Id", "Label", "Color"]:
        table.add_column(h, no_wrap=True, header_style="bold blue")
    try:
        for row in rows:
            color = str(row["color"]).lower()
            table.add_row(
                str(row["id"]), str(row["label"]), Text(color, style=f"on {color}")
            )
        console.print(table, justify="center")
    except Exception as e:
        ctx.obj.logger.fatal(str(e))
