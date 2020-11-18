#!/usr/bin/env python3
import click
import click_completion
from pyintelowl.pyintelowl import IntelOwl
from pyintelowl.cli import groups, cmds
from pyintelowl.cli._utils import get_logger, ClickContext, get_netrc_obj


# Enable auto completion
click_completion.init()


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-d", "--debug", is_flag=True, help="Set log level to DEBUG")
@click.pass_context
def cli(ctx: ClickContext, debug: bool):
    netrc, host = get_netrc_obj()
    api_key, url, cert = host["password"], host["account"], host["login"]
    if not api_key or not url:
        click.echo("Hint: Use `config set` to set config variables!")
    else:
        logger = get_logger("DEBUG" if debug else "INFO")
        ctx.obj = IntelOwl(api_key, url, cert, logger)


# Compile all groups and commands
for c in groups + cmds:
    cli.add_command(c)

# Entrypoint/executor
if __name__ == "__main__":
    cli()
