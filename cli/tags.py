import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box, print as rprint

from ._utils import ClickContext


@click.command(short_help="Manage tags")
@click.option("-a", "--all", is_flag=True, help="List all tags")
@click.option("--id", type=int, default=0, help="Retrieve tag details by ID")
@click.pass_context
def tags(ctx: ClickContext, id: int, all: bool):
    """
    Manage tags
    """
    if all:
        ans, errs = ctx.obj.get_all_tags()
    elif id:
        ans, errs = ctx.obj.get_tag_by_id(id)
        ans = [ans]
    if errs:
        rprint(errs)
    else:
        _print_tags_table(ans)


def _print_tags_table(data):
    console = Console()
    table = Table(show_header=True, title="List of tags", box=box.DOUBLE_EDGE)
    table.add_column("Id", no_wrap=True, header_style="bold blue")
    table.add_column("Label", no_wrap=True, header_style="bold blue")
    table.add_column("Color", no_wrap=True, header_style="bold blue")
    try:
        for elem in data:
            color = str(elem["color"]).lower()
            table.add_row(
                str(elem["id"]),
                str(elem["label"]),
                Text(color, style=f"on {color}")
            )
        console.print(table, justify="center")
    except Exception as e:
        rprint(e)
