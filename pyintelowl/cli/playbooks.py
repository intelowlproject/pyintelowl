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
    get_success_text,
    json_flag_option,
)


@click.group(help="Manage playbooks")
def playbooks():
    pass


def _display_playbook(data):
    style = "[bold #31DDCF]"
    tags = ", ".join(
        data["tags"]
    )  # this is a [str], not a complex object like in job API
    console = Console()
    console.print(data)
    r = Group(
        f"{style}Playbook ID:[/] {str(data['id'])}",
        f"{style}Name:[/] {data['name']}",
        f"{style}Tags:[/] {tags}",
        f"{style}TLP:[/] {data['tlp']}",
        f"{style}Analyzers:[/] {data['analyzers']}",
        f"{style}Connectors:[/] {data['connectors']}",
        f"{style}Pivots:[/] {data['pivots']}",
        f"{style}Visualizers:[/] {data['visualizers']}",
        f"{style}Runtime configuration:[/] {data['runtime_configuration']}",
        f"{style}For Organizations:[/] {data['for_organization']}",
        f"{style}Disabled:[/] {data['disabled']}",
        f"{style}Starting:[/] {data['starting']}",
        f"{style}Description:[/] {data['description']}",
    )
    return Panel(r, title="Playbook attributes")


@playbooks.command(help="Tabular print playbook attributes for a playbook name")
@click.argument("playbook_name", type=str)
@add_options(json_flag_option)
@click.pass_context
def view(
    ctx: ClickContext,
    playbook_name: str,
    as_json: bool,
):
    ctx.obj.logger.info(f"Requesting Playbook [underline blue]{playbook_name}[/]..")
    try:
        ans = ctx.obj.get_playbook_by_name(playbook_name)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))

    if as_json:
        rprint(json.dumps(ans, indent=4))
    else:
        _display_playbook(ans)


def _display_all_playbooks(logger, rows):
    console = Console()
    table = Table(show_header=True, title="List of Playbooks", box=box.DOUBLE_EDGE)
    header_style = "bold blue"
    headers: [] = [
        "id",
        "name",
        "tags",
        "tlp",
        "analyzers",
        "connectors",
        "pivots",
        "visualizers",
        "runtime_configuration",
        "for_organization",
        "disabled",
        "starting",
        "description",
    ]
    [table.add_column(header=header, header_style=header_style) for header in headers]
    try:
        for el in rows:
            table.add_row(
                str(el["id"]),
                el["name"],
                ", ".join([str(tag) for tag in el["tags"]]),
                el["tlp"],
                ", ".join([str(tag) for tag in el["analyzers"]]),
                ", ".join([str(tag) for tag in el["connectors"]]),
                ", ".join([str(tag) for tag in el["pivots"]]),
                ", ".join([str(tag) for tag in el["visualizers"]]),
                str(el["runtime_configuration"]),
                get_success_text(el["for_organization"]),
                get_success_text(el["disabled"]),
                get_success_text(el["starting"]),
                el["description"],
            )
        console.print(table, justify="center")
    except Exception as e:
        logger.fatal(e, exc_info=True)


@playbooks.command(help="List all playbooks")
@add_options(json_flag_option)
@click.pass_context
def ls(ctx: ClickContext, as_json: bool):
    ctx.obj.logger.info("Requesting list of playbooks..")
    try:
        ans = ctx.obj.get_all_playbooks()
        results = ans.get("results", [])
        ctx.obj.logger.info(results)
        if as_json:
            rprint(json.dumps(results, indent=4))
        else:
            _display_all_playbooks(ctx.obj.logger, results)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
