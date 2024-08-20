import click
from rich import print as rprint

from pyintelowl.pyintelowl import IntelOwlClientException

from ..cli._utils import ClickContext, get_success_text


@click.command(help="Send healthcheck request for an analyzer (docker-based)")
@click.argument("analyzer_name", type=str)
@click.pass_context
def analyzer_healthcheck(ctx: ClickContext, analyzer_name: str):
    ctx.obj.logger.info(
        f"Requesting healthcheck for analyzer [underline blue]{analyzer_name}[/]"
    )
    try:
        status = ctx.obj.analyzer_healthcheck(analyzer_name)
        if status is True:
            rprint(f"healthy {get_success_text(str(True))}")
        elif status is False:
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
        f"Requesting healthcheck for connector [underline blue]{connector_name}[/]"
    )
    try:
        status = ctx.obj.connector_healthcheck(connector_name)
        if status is True:
            rprint(f"healthy {get_success_text(str(True))}")
        elif status is False:
            rprint(f"failing {get_success_text(str(False))}")
        else:
            rprint("unknown")
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
