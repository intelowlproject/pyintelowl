import click
from ._utils import add_options, ClickContext

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
    run_all_available_analyzers,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
):
    if not analyzers_list:
        if not run_all_available_analyzers:
            click.echo(
                """
                One of --analyzers-list,
                --run-all-available-analyzers should be specified
                """,
                err=True,
                color="RED",
            )
    ans, errs = ctx.obj.send_observable_analysis_request(
        analyzers_requested=analyzers_list,
        observable_name=value,
        force_privacy=force_privacy,
        private_job=private_job,
        disable_external_analyzers=disable_external_analyzers,
        run_all_available_analyzers=run_all_available_analyzers,
    )


@analyse.command(short_help="Send analysis request for a file")
@click.argument("filename", type=click.Path(exists=True))
@add_options(__analyse_options)
@click.pass_context
def file(
    ctx: ClickContext,
    filename,
    analyzers_list,
    run_all_available_analyzers,
    force_privacy,
    private_job,
    disable_external_analyzers,
    check,
):
    pass
