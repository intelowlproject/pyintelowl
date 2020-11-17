import click
from rich import print as rprint

from ._utils import get_netrc_obj


@click.group("config")
def config():
    """
    Set or view config variables
    """
    pass


@config.command("get")
def config_get():
    """
    Pretty Print config variables
    """
    _, host = get_netrc_obj()
    rprint({
        "api_key": host["password"],
        "instance_url": host["account"],
        "certificate": host["login"],
    })


@config.command("set")
@click.option(
    "-k",
    "--api-key",
    required=True,
    help="API key to authenticate against a IntelOwl instance",
)
@click.option(
    "-u",
    "--instance-url",
    required=True,
    default="http://localhost:80",
    show_default=True,
    help="IntelOwl's instance URL",
)
@click.option(
    "-c",
    "--certificate",
    required=False,
    type=click.Path(exists=True),
    help="Path to SSL client certificate file (.pem)",
)
def config_set(api_key, instance_url, certificate):
    """
    Set/Edit config variables
    """
    netrc, _ = get_netrc_obj()
    if api_key:
        netrc["pyintelowl"]["password"] = api_key
    if instance_url:
        netrc["pyintelowl"]["account"] = instance_url
    if certificate:
        netrc["pyintelowl"]["login"] = certificate
    # finally save
    netrc.save()
