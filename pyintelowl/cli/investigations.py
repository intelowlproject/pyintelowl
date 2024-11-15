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


def _display_all_investigations(logger, rows):
    console = Console()
    table = Table(show_header=True, title="List of Investigations", box=box.DOUBLE_EDGE)
    header_style = "bold blue"
    headers: [] = [
        "Id",
        "Name",
        "Tags",
        "Description",
        "Owner",
        "TLP",
        "Total jobs",
        "Jobs",
        "Status",
    ]
    [table.add_column(header=header, header_style=header_style) for header in headers]
    try:
        for el in rows:
            table.add_row(
                str(el["id"]),
                el["name"],
                ", ".join([str(tag) for tag in el["tags"]]),
                el["description"],
                el["owner"],
                el["tlp"],
                str(el["total_jobs"]),
                ", ".join([str(job_id) for job_id in el["jobs"]]),
                el["status"],
            )
        console.print(table, justify="center")
    except Exception as e:
        logger.fatal(e, exc_info=True)


@investigations.command(help="Delete job from investigation by their ID")
@click.argument("investigation_id", type=int)
@click.argument("job_id", type=int)
@click.pass_context
def rm(ctx: ClickContext, investigation_id: int, job_id: int):
    ctx.obj.logger.info(
        f"Requesting delete for Job [underline blue]#{job_id}[/] "
        f"from Investigation #[underline blue]#{investigation_id}[/].."
    )
    try:
        ctx.obj.delete_job_from_investigation(investigation_id, job_id)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@investigations.command(
    help="Add existing job to an existing investigation by their ID"
)
@click.argument("investigation_id", type=int)
@click.argument("job_id", type=int)
@click.pass_context
def add(ctx: ClickContext, investigation_id: int, job_id: int):
    ctx.obj.logger.info(
        f"Requesting add for Job [underline blue]#{job_id}[/] "
        f"to Investigation #[underline blue]#{investigation_id}[/].."
    )
    try:
        ctx.obj.add_job_to_investigation(investigation_id, job_id)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


def _render_investigation_attributes(data):
    style = "[bold #31DDCF]"
    tags = ", ".join(
        data["tags"]
    )  # this is a [str], not a complex object like in job API
    status: str = get_status_text(data["status"], as_text=False)
    console = Console()
    console.print(data)
    r = Group(
        f"{style}Investigation ID:[/] {str(data['id'])}",
        f"{style}Name:[/] {data['name']}",
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
@add_options(json_flag_option)
@click.pass_context
def view(
    ctx: ClickContext,
    investigation_id: int,
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
@add_options(json_flag_option)
@click.pass_context
def view_tree(
    ctx: ClickContext,
    investigation_id: int,
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


@investigations.command(help="List all investigations")
@click.option(
    "--status",
    type=click.Choice(
        ["created", "running", "concluded"],
        case_sensitive=False,
    ),
    show_choices=True,
    help="Only show investigations having a particular status",
)
@add_options(json_flag_option)
@click.pass_context
def ls(ctx: ClickContext, status: str, as_json: bool):
    ctx.obj.logger.info("Requesting list of investigations..")
    try:
        ans = ctx.obj.get_all_investigations()
        results = ans.get("results", [])
        ctx.obj.logger.info(results)
        if status:
            results = [el for el in results if el["status"].lower() == status.lower()]
        if as_json:
            rprint(json.dumps(results, indent=4))
        else:
            _display_all_investigations(ctx.obj.logger, results)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
