import click
import json
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich import print as rprint

from pyintelowl.exceptions import IntelOwlClientException

from ..cli._utils import ClickContext, add_options, json_flag_option


@click.group(help="Manage tags")
def tags():
    pass


@tags.command(help="List all tags")
@add_options(json_flag_option)
@click.pass_context
def ls(ctx: ClickContext, as_json: bool):
    try:
        ans = ctx.obj.get_all_tags()
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _print_tags_table(ctx.obj.logger, ans)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@tags.command(help="Retrieve tag details by ID")
@click.argument("id", type=int)
@add_options(json_flag_option)
@click.pass_context
def view(ctx: ClickContext, id: int, as_json: bool):
    try:
        ans = ctx.obj.get_tag_by_id(id)
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            ans = [ans]
            _print_tags_table(ctx.obj.logger, ans)
    except IntelOwlClientException as e:
        print(e.response.status_code)
        ctx.obj.logger.fatal(str(e))


def _print_tags_table(logger, rows):
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
        logger.fatal(str(e))
