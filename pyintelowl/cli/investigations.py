import json

import click
from rich import box
from rich import print as rprint
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from pyintelowl import IntelOwlClientException
from pyintelowl.cli._utils import (
    ClickContext,
    add_options,
    get_json_syntax,
    get_status_text,
    json_flag_option,
)


@click.group(help="Manage investigations")
def investigations():
    pass


def _render_investigation_attributes(data):
    style = "[bold #31DDCF]"
    tags = ", ".join(data["tags"])
    status: str = get_status_text(data["status"], as_text=False)
    console = Console()
    console.print(data)
    r = Group(
        f"{style}Investigation ID:[/] {str(data['id'])}",
        f"{style}Name:[/] {data["name"]}",
        f"{style}Tags:[/] {tags}",
        f"{style}Status:[/] {status}",
        f"{style}TLP:[/] {data['tlp']}",
        f"{style}Total jobs:[/] {data['total_jobs']}",
        f"{style}Jobs ID:[/] {data['jobs']}",
        f"{style}Description:[/] {data['description']}",
    )
    return Panel(r, title="Investigation attributes")


def _render_investigation_table(data, title: str):
    headers = ["Name", "Owner", "Jobs"]
    table = Table(
        show_header=True,
        title=title,
        box=box.DOUBLE_EDGE,
        show_lines=True,
    )
    # add headers
    for h in headers:
        table.add_column(h, header_style="bold blue")

    # retrieve all jobs and childrens
    table.add_row(
        data.get("name", ""),
        str(data.get("owner", "")),
        get_json_syntax(data.get("jobs", [])),
    )
    return table


def _display_investigation(data):
    console = Console()
    attrs = _render_investigation_attributes(data)
    with console.pager(styles=True):
        console.print(attrs)


def _display_investigation_tree(data):
    console = Console()
    table = _render_investigation_table(data, title="Investigation report")
    with console.pager(styles=True):
        console.print(table, justify="center")


@investigations.command(
    help="Tabular print investigation attributes and results for an investigation ID"
)
@click.argument("investigation_id", type=int)
@click.option(
    "-r",
    "--report",
    type=click.Choice(
        [
            "analyzers",
            "connectors",
        ]
    ),
    default="analyzers",
    show_choices=True,
    help="""
    Choose the type of report to be displayed:
    analyzer or connector.
    """,
)
@add_options(json_flag_option)
@click.pass_context
def view(
    ctx: ClickContext,
    investigation_id: int,
    report: str,
    as_json: bool,
):
    ctx.obj.logger.info(
        f"Requesting Investigation [underline blue]#{investigation_id}[/].."
    )
    try:
        ans = ctx.obj.get_investigation_by_id(investigation_id)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))

    if as_json:
        rprint(json.dumps(ans, indent=4))
    else:
        _display_investigation(ans)


@investigations.command(
    help="Tabular print investigation's tree structure for an investigation ID"
)
@click.argument("investigation_id", type=int)
@click.option(
    "-r",
    "--report",
    type=click.Choice(
        [
            "analyzers",
            "connectors",
        ]
    ),
    default="analyzers",
    show_choices=True,
    help="""
    Choose the type of report to be displayed:
    analyzer or connector.
    """,
)
@add_options(json_flag_option)
@click.pass_context
def view_tree(
    ctx: ClickContext,
    investigation_id: int,
    report: str,
    as_json: bool,
):
    ctx.obj.logger.info(
        f"Requesting Investigation tree [underline blue]#{investigation_id}[/].."
    )
    try:
        ans = ctx.obj.get_investigation_tree_by_id(investigation_id)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))

    if as_json:
        rprint(json.dumps(ans, indent=4))
    else:
        _display_investigation_tree(ans)
