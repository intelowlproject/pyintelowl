#!/usr/bin/env python3
import click
import click_creds

from .cli import cmds, groups
from .cli._utils import ClickContext, get_logger, get_version_number
from .pyintelowl import IntelOwl


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-d", "--debug", is_flag=True, help="Set log level to DEBUG")
@click.version_option(version=get_version_number())
@click_creds.use_netrcstore(
    name="pyintelowl",
    mapping={"login": "certificate", "password": "api_key", "account": "instance_url"},
)
@click.pass_context
def cli(ctx: ClickContext, debug: bool):
    host = click_creds.get_netrc_object_from_ctx(ctx).host.copy()
    api_key, url, cert = host["password"], host["account"], host["login"]
    if (not api_key or not url) and ctx.invoked_subcommand != "config":
        click.echo("Hint: Use `config set` to set config variables!")
        exit()
    else:
        logger = get_logger("DEBUG" if debug else "INFO")
        if cert == "False":
            cert = False
        elif cert in ["None", "True"]:
            cert = True
        ctx.obj = IntelOwl(api_key, url, cert, {}, logger, cli=True)


# Compile all groups and commands
for c in groups + cmds:
    cli.add_command(c)

# Entrypoint/executor
if __name__ == "__main__":
    cli()
