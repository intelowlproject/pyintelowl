import click
from ._utils import add_options, ClickContext
from .jobs import _display_single_job

__analyse_options = [
    click.option(
        "-al",
        "--analyzers-list",
        multiple=True,
        type=str,
        default=(),
        help="""
    List of analyzer names to invoke. Should not be used with
    --run-all-available-analyzers
    """,
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
]


@click.group("analyse")
def analyse():
    """
    Send new analysis request
    """
    pass


@analyse.command(short_help="Send analysis request for an observable")
@click.argument("value")
@add_options(__analyse_options)
@click.pass_context
def observable(
    ctx: ClickContext,
    value,
    analyzers_list,
    run_all,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
):
    if analyzers_list and run_all:
        logger.warn(
            """
            Can't use -al and -aa options together. See usage with -h.
            """
        )
        ctx.exit(-1)
    if not (analyzers_list or run_all):
        logger.warn(
            """
            Either one of -al, -aa must be specified. See usage with -h.
            """,
        )
        ctx.exit(-1)
    analyzers = analyzers_list if analyzers_list else "all available analyzers"
    ctx.obj.logger.info(
        f"""Requesting analysis..
        observable: [bold blue underline]{value}[/]
        analyzers: [italic green]{analyzers}[/]
        """,
    )
    # first step: ask analysis availability
    ans = ctx.obj.send_observable_analysis_request(
        analyzers_requested=analyzers_list,
        observable_name=value,
        force_privacy=force_privacy,
        private_job=private_job,
        disable_external_analyzers=disable_external_analyzers,
        run_all_available_analyzers=run_all,
    )
    warnings = ans["warnings"]
    ctx.obj.logger.info(
        f"""New Job running..
        ID: {ans['job_id']} | Status: [underline pink]{ans['status']}[/].
        Got {len(warnings)} warnings: [italic red]{warnings if warnings else None}[/]
    """
    )


@analyse.command(short_help="Send analysis request for a file")
@click.argument("filename", type=click.Path(exists=True))
@add_options(__analyse_options)
@click.pass_context
def file(
    ctx: ClickContext,
    filename,
    analyzers_list,
    run_all,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
):
    pass
