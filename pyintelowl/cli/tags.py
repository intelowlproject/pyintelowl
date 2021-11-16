import json

import click
from rich import box
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.text import Text

from pyintelowl.exceptions import IntelOwlClientException

from ..cli._utils import (
    ClickContext,
    add_options,
    get_action_status_text,
    json_flag_option,
)


@click.group(help="Manage tags")
def tags():
    pass


@tags.command(help="List all tags")
@add_options(json_flag_option)
@click.pass_context
def ls(ctx: ClickContext, as_json: bool):
    ctx.obj.logger.info("Requesting list of tags..")
    try:
        ans = ctx.obj.get_all_tags()
        ans.sort(key=lambda tag: tag["id"])
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _print_tags_table(ctx.obj.logger, ans)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@tags.command(help="Create new Tag")
@click.argument("label", type=str)
@click.argument("color", type=str)
@add_options(json_flag_option)
@click.pass_context
def new(ctx: ClickContext, as_json: bool, color: str, label: str):
    ctx.obj.logger.info("Adding new Tag..")
    try:
        ans = ctx.obj.create_tag(label, color)
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _print_tags_table(ctx.obj.logger, [ans])
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@tags.command(help="Edit existing Tag attributes")
@click.argument("tag_id", type=int)
@click.argument("label", type=str)
@click.argument("color", type=str)
@add_options(json_flag_option)
@click.pass_context
def edit(ctx: ClickContext, as_json: bool, color: str, label: str, tag_id: int):
    ctx.obj.logger.info("Updating new Tag..")
    try:
        ans = ctx.obj.edit_tag(tag_id, label, color)
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _print_tags_table(ctx.obj.logger, [ans])
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@tags.command(help="Retrieve tag details by ID")
@click.argument("tag_id", type=int)
@add_options(json_flag_option)
@click.pass_context
def view(ctx: ClickContext, tag_id: int, as_json: bool):
    ctx.obj.logger.info(f"Requesting Tag [underline blue]#{tag_id}[/]..")
    try:
        ans = ctx.obj.get_tag_by_id(tag_id)
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _print_tags_table(ctx.obj.logger, [ans])
    except IntelOwlClientException as e:
        print(e.response.status_code)
        ctx.obj.logger.fatal(str(e))


@tags.command(help="Delete tag by tag ID")
@click.argument("tag_id", type=int)
@click.pass_context
def rm(ctx: ClickContext, tag_id: int):
    ctx.obj.logger.info(f"Requesting delete for tag [underline blue]#{tag_id}[/]..")
    ans = False
    try:
        ans = ctx.obj.delete_tag_by_id(tag_id)
        rprint(get_action_status_text(ans, "delete"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "delete"))
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
