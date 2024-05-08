import click

from pyintelowl.exceptions import IntelOwlClientException

from ..cli._utils import ClickContext, add_options, get_json_data

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
        type=click.Choice(
            ["WHITE", "CLEAR", "GREEN", "AMBER", "RED"], case_sensitive=False
        ),
        help="TLP for the analysis (WHITE/CLEAR/GREEN/AMBER/RED)",
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
        "-m",
        "--check-minutes-ago",
        type=int,
        default=None,
        help="Number of minutes ago to check for"
        " a previous analysis. Default infinity.",
    ),
    click.option(
        "-r",
        "--runtime-config",
        help="Path to JSON file which contains runtime_configuration.",
        type=click.Path(exists=True, resolve_path=True),
    ),
    click.option(
        "-p",
        "--poll",
        "should_poll",
        is_flag=True,
        help="HTTP poll for the job result and notify when it's finished",
    ),
]

__playbook_analyse_options = __analyse_options.copy()
# doing it twice to remove --analyzers-list and --connectors-list
__playbook_analyse_options.pop(0)
__playbook_analyse_options.pop(0)
__playbook_analyse_options.pop(3)
__playbook_analyse_options.pop(2)


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
    check_minutes_ago: int,
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
            check_minutes_ago,
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
    check_minutes_ago: int,
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
            check_minutes_ago,
        )
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@analyse.command(help="Send playbook analysis request for an observable")
@click.argument("value")
@click.argument("playbook")
@add_options(__playbook_analyse_options)
@click.pass_context
def playbook_observable(
    ctx: ClickContext,
    value: str,
    playbook: str,
    tags_list: str,
    tlp: str,
    runtime_config,
    should_poll: bool,
):
    tags_labels = tags_list.split(",") if len(tags_list) else []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        print("here")
        ctx.obj._new_analysis_playbook_cli(
            value,
            "observable",
            playbook,
            tlp,
            runtime_config,
            tags_labels,
            should_poll,
        )
        print("here3")
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@analyse.command(help="Send playbook analysis request for an observable")
@click.argument("filepath", type=click.Path(exists=True, resolve_path=True))
@click.argument("playbook")
@add_options(__playbook_analyse_options)
@click.pass_context
def playbook_file(
    ctx: ClickContext,
    filepath: str,
    playbook: str,
    tags_list: str,
    tlp: str,
    runtime_config,
    should_poll: bool,
):
    tags_labels = tags_list.split(",") if len(tags_list) else []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        ctx.obj._new_analysis_playbook_cli(
            filepath,
            "file",
            playbook,
            tlp,
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
