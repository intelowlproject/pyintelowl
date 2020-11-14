import click
from pyintelowl.pyintelowl import IntelOwl
from cli import groups, cmds


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-k",
    "--api-key",
    required=True,
    default="",
    help="API key to authenticate against a IntelOwl instance",
)
@click.option(
    "-u",
    "--instance-url",
    required=True,
    default="http://localhost:80",
    help="IntelOwl's instance URL",
)
@click.option(
    "-c",
    "--certificate",
    required=False,
    type=click.Path(exists=True),
    help="Path to SSL client certificate file (.pem)",
)
@click.option("--debug/--no-debug", default=False, help="Set log level to DEBUG")
@click.pass_context
def cli(ctx, api_key, instance_url, certificate, debug):
    ctx.obj: "IntelOwl" = IntelOwl(api_key, instance_url, certificate, debug)


# Compile all groups and commands
for c in groups + cmds:
    cli.add_command(c)


# Entrypoint/executor
if __name__ == "__main__":
    cli()
