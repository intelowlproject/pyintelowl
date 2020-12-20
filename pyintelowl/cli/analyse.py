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
    Comma separated list of analyzer names to invoke. Should not be used with
    --run-all-available-analyzers
    """,
    ),
    click.option(
        "-tl",
        "--tags-list",
        type=str,
        default="",
        help="Comma separated list of tag indices for respective job.",
    ),
    click.option(
        "-aa",
        "--run-all-available-analyzers",
        "run_all",
        is_flag=True,
        help="""
    Run all available and compatible analyzers. Should not be used with
    --analyzers-list.
    """,
    ),
    click.option(
        "-fp",
        "--force-privacy",
        is_flag=True,
        help="Disable analyzers that could impact privacy",
    ),
    click.option(
        "-p",
        "--private-job",
        is_flag=True,
        help="Limit view permissions to my group",
    ),
    click.option(
        "-de",
        "--disable-external-analyzers",
        is_flag=True,
        help="Disable analyzers that use external services",
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
    value,
    analyzers_list: str,
    tags_list: str,
    run_all,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
    runtime_config,
    should_poll: bool,
):
    if not run_all:
        analyzers_list = analyzers_list.split(",")
    else:
        analyzers_list = []
    if tags_list:
        tags_list = list(map(int, tags_list.split(",")))
    else:
        tags_list = []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        ctx.obj._new_analysis_cli(
            value,
            "observable",
            analyzers_list,
            tags_list,
            run_all,
            force_privacy,
            private_job,
            disable_external_analyzers,
            check,
            runtime_config,
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
    tags_list: str,
    run_all,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
    runtime_config,
    should_poll: bool,
):
    if not run_all:
        analyzers_list = analyzers_list.split(",")
    else:
        analyzers_list = []
    if tags_list:
        tags_list = list(map(int, tags_list.split(",")))
    else:
        tags_list = []
    if runtime_config:
        runtime_config = get_json_data(runtime_config)
    else:
        runtime_config = {}
    try:
        ctx.obj._new_analysis_cli(
            filepath,
            "file",
            analyzers_list,
            tags_list,
            run_all,
            force_privacy,
            private_job,
            disable_external_analyzers,
            check,
            runtime_config,
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
    # parse boolean columns
    bool_flags = [
        "run_all",
        "force_privacy",
        "private_job",
        "disable_external_analyzers",
    ]
    for row in rows:
        for flag in bool_flags:
            row[flag] = row.get(flag, False) in ["true", True]
    try:
        ctx.obj.send_analysis_batch(rows)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))
