import click
import json
import re
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print as rprint

from ..cli._utils import (
    ClickContext,
    get_success_text,
    get_json_syntax,
    add_options,
    json_flag_option,
)
from pyintelowl.pyintelowl import IntelOwlClientException


@click.command(
    help="Get current state of `analyzer_config.json` from the IntelOwl instance",
)
@click.option(
    "-m",
    "--re-match",
    help="RegEx Pattern to filter analyzer names against",
)
@add_options(json_flag_option)
@click.option(
    "-t", "--text", "as_text", is_flag=True, help="Print analyzer names as CSV"
)
@click.pass_context
def get_analyzer_config(ctx: ClickContext, re_match: str, as_json: bool, as_text: bool):
    console = Console()
    ctx.obj.logger.info("Requesting [italic blue]analyzer_config.json[/]..")
    try:
        res = ctx.obj.get_analyzer_configs()
        # filter resulset if a regex pattern was provided
        if re_match:
            pat = re.compile(re_match)
            res = {k: v for k, v in res.items() if pat.match(k) is not None}
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
        ctx.exit(0)
    if as_json:
        with console.pager(styles=True):
            console.print(json.dumps(res, indent=4))
    elif as_text:
        click.echo(", ".join(res.keys()))
    else:
        # otherwise, print full table
        headers = [
            "Name",
            "Type",
            "Description",
            "Supported\nTypes",
            "External\nService",
            "Leaks\nInfo",
            "Configuration\nParameters",
            "Secrets",
            "Configured",
        ]
        header_style = "bold blue"
        table = Table(
            show_header=True,
            title="Analyzer Configurations",
            box=box.DOUBLE_EDGE,
            show_lines=True,
        )
        for h in headers:
            table.add_column(h, header_style=header_style, justify="center")
        for name, obj in res.items():
            table.add_row(
                name,
                obj["type"],
                obj.get("description", ""),
                get_json_syntax(
                    obj.get(
                        "observable_supported",
                        obj.get("supported_filetypes", []),
                    )
                ),
                get_success_text(obj.get("external_service", False)),
                get_success_text(obj.get("leaks_info", False)),
                get_json_syntax(obj.get("config", {})),
                get_json_syntax(obj.get("secrets", {})),
                get_success_text(obj["verification"].get("configured", False)),
            )
        with console.pager(styles=True):
            console.print(table)


@click.command(
    help="Get current state of `connector_config.json` from the IntelOwl instance",
)
@click.option(
    "-m",
    "--re-match",
    help="RegEx Pattern to filter connector names against",
)
@add_options(json_flag_option)
@click.option(
    "-t", "--text", "as_text", is_flag=True, help="Print connector names as CSV"
)
@click.pass_context
def get_connector_config(
    ctx: ClickContext, re_match: str, as_json: bool, as_text: bool
):
    console = Console()
    ctx.obj.logger.info("Requesting [italic blue]connector_config.json[/]..")
    try:
        res = ctx.obj.get_connector_configs()
        # filter resulset if a regex pattern was provided
        if re_match:
            pat = re.compile(re_match)
            res = {k: v for k, v in res.items() if pat.match(k) is not None}
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
        ctx.exit(0)
    if as_json:
        with console.pager(styles=True):
            console.print(json.dumps(res, indent=4))
    elif as_text:
        click.echo(", ".join(res.keys()))
    else:
        # otherwise, print full table
        headers = [
            "Name",
            "Description",
            "Configuration\nParameters",
            "Secrets",
            "Configured",
        ]
        header_style = "bold blue"
        table = Table(
            show_header=True,
            title="Connector Configurations",
            box=box.DOUBLE_EDGE,
            show_lines=True,
        )
        for h in headers:
            table.add_column(h, header_style=header_style, justify="center")
        for name, obj in res.items():
            table.add_row(
                name,
                obj.get("description", ""),
                get_json_syntax(obj.get("config", {})),
                get_json_syntax(obj.get("secrets", {})),
                get_success_text(obj["verification"].get("configured", False)),
            )
        with console.pager(styles=True):
            console.print(table)


@click.command(help="Send healthcheck request for an analyzer (docker-based)")
@click.argument("analyzer_name", type=str)
@click.pass_context
def analyzer_healthcheck(ctx: ClickContext, analyzer_name: str):
    ctx.obj.logger.info(
        f"Requesting healthcheck for analyzer [underline blue]#{analyzer_name}[/]"
    )
    try:
        result = ctx.obj.analyzer_healthcheck(analyzer_name)
        if result["status"] is True:
            rprint(f"healthy {get_success_text(str(True))}")
        elif result["status"] is False:
            rprint(f"failing {get_success_text(str(False))}")
        else:
            rprint("unknown")
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@click.command(help="Send healthcheck request for a connector")
@click.argument("connector_name", type=str)
@click.pass_context
def connector_healthcheck(ctx: ClickContext, connector_name: str):
    ctx.obj.logger.info(
        f"Requesting healthcheck for connector [underline blue]#{connector_name}[/]"
    )
    try:
        result = ctx.obj.connector_healthcheck(connector_name)
        if result["status"] is True:
            rprint(f"healthy {get_success_text(str(True))}")
        elif result["status"] is False:
            rprint(f"failing {get_success_text(str(False))}")
        else:
            rprint("unknown")
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
