import click

from pyintelowl.exceptions import IntelOwlClientException
from ..cli._utils import add_options, ClickContext, get_json_data

__analyse_options = [
    click.option(
        "-al",
        "--analyzers-list",
        type=str,
        default="",
        help="""
    Comma separated list of analyzer names to invoke.
    Defaults to all configured analyzers.
    """,
    ),
    click.option(
        "-cl",
        "--connectors-list",
        type=str,
        default="",
        help="""
    Comma separated list of connector names to invoke.
    Defaults to all configured connectors.
    """,
    ),
    click.option(
        "-tl",
        "--tags-list",
        type=str,
        default="",
        help="Comma separated list of tag labels to assign (creates non-existing tags)",
    ),
    click.option(
        "-t",
        "--tlp",
        type=click.Choice(["WHITE", "GREEN", "AMBER", "RED"], case_sensitive=False),
        help="TLP for the analysis (WHITE/GREEN/AMBER/RED)",
    ),
    click.option(
        "-c",
        "--check",
        type=click.Choice(["reported", "running", "force-new"], case_sensitive=False),
        default="reported",
        show_choices=True,
        show_default=True,
        help="""\n
    1. 'reported': analysis won't be repeated if already exists as running or failed.\n
    2. 'running': analysis won't be repeated if already running.\n
    3. 'force_new': force new analysis
    """,
    ),
    click.option(
        "-r",
        "--runtime-config",
        help="Path to JSON file which contains runtime_configuration.",
        type=click.Path(exists=True, resolve_path=True),
    ),
    click.option(
        "--poll",
        "should_poll",
        is_flag=True,
        help="HTTP poll for the job result and notify when it's finished",
    ),
]


@click.group("analyse")
def analyse():
    """
    Send new analysis request
    """


@analyse.command(help="Send analysis request for an observable")
@click.argument("value")
@add_options(__analyse_options)
@click.pass_context
def observable(
    ctx: ClickContext,
    value: str,
    analyzers_list: str,
    connectors_list: str,
    tags_list: str,
    tlp: str,
    check,
    runtime_config,
    should_poll: bool,
):
    analyzers_list = analyzers_list.split(",") if len(analyzers_list) else []
    connectors_list = connectors_list.split(",") if len(connectors_list) else []
    tags_labels = tags_list.split(",") if len(tags_list) else []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        ctx.obj._new_analysis_cli(
            value,
            "observable",
            check,
            tlp,
            analyzers_list,
            connectors_list,
            runtime_config,
            tags_labels,
            should_poll,
        )
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@analyse.command(help="Send analysis request for a file")
@click.argument("filepath", type=click.Path(exists=True, resolve_path=True))
@add_options(__analyse_options)
@click.pass_context
def file(
    ctx: ClickContext,
    filepath: str,
    analyzers_list: str,
    connectors_list: str,
    tags_list: str,
    tlp: str,
    check,
    runtime_config,
    should_poll: bool,
):
    analyzers_list = analyzers_list.split(",") if len(analyzers_list) else []
    connectors_list = connectors_list.split(",") if len(connectors_list) else []
    tags_labels = tags_list.split(",") if len(tags_list) else []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        ctx.obj._new_analysis_cli(
            filepath,
            "file",
            check,
            tlp,
            analyzers_list,
            connectors_list,
            runtime_config,
            tags_labels,
            should_poll,
        )
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@analyse.command(
    help="Send multiple analysis requests. Reads file (csv or json) for inputs."
)
@click.argument("filepath", type=click.Path(exists=True, resolve_path=True))
@click.pass_context
def batch(
    ctx: ClickContext,
    filepath: str,
):
    rows = get_json_data(filepath)
    try:
        ctx.obj.send_analysis_batch(rows)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
