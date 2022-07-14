import json

import click
from rich import print as rprint
from rich.console import Console

from pyintelowl.exceptions import IntelOwlClientException

from ..cli._jobs_utils import (
    _display_all_jobs,
    _display_single_job,
    _poll_for_job_cli,
    _result_filter_and_tabular_print,
)
from ..cli._utils import (
    ClickContext,
    add_options,
    get_action_status_text,
    json_flag_option,
)


@click.group("jobs", help="Manage Jobs")
def jobs():
    pass


@jobs.command(help="List all jobs")
@click.option(
    "--status",
    type=click.Choice(
        [
            "pending",
            "running",
            "reported_without_fails",
            "reported_with_fails",
            "failed",
            "killed",
        ],
        case_sensitive=False,
    ),
    show_choices=True,
    help="Only show jobs having a particular status",
)
@add_options(json_flag_option)
@click.pass_context
def ls(ctx: ClickContext, status: str, as_json: bool):
    ctx.obj.logger.info("Requesting list of jobs..")
    try:
        ans = ctx.obj.get_all_jobs()
        results = ans.get("results", [])
        ctx.obj.logger.info(results)
        if status:
            ans = [el for el in results if el["status"].lower() == status.lower()]
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _display_all_jobs(ctx.obj.logger, results)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Tabular print job attributes and results for a job ID")
@click.argument("job_id", type=int)
@click.option(
    "-r",
    "--report",
    type=click.Choice(
        [
            "analyzers",
            "connectors",
        ]
    ),
    default="analyzers",
    show_choices=True,
    help="""
    Choose the type of report to be displayed:
    analyzer or connector.
    """,
)
@click.option(
    "-c",
    "--categorize",
    is_flag=True,
    help="""
    Categorize results according to type and analyzer.
    Only works for observable analysis.
    """,
)
@add_options(json_flag_option)
@click.pass_context
def view(ctx: ClickContext, job_id: int, report: str, categorize: bool, as_json: bool):
    ctx.obj.logger.info(f"Requesting Job [underline blue]#{job_id}[/]..")
    if as_json and categorize:
        raise click.Abort("Cannot use the -c and -j options together")
    try:
        ans = ctx.obj.get_job_by_id(job_id)
        report_type = (
            "analyzer_reports" if report == "analyzers" else "connector_reports"
        )
        if as_json:
            rprint(json.dumps(ans, indent=4))
        elif categorize:
            if ans["is_sample"]:
                raise click.Abort("Cannot use the -c option for a file analysis")
            _result_filter_and_tabular_print(
                ans[report_type],
                ans["observable_name"],
                ans["observable_classification"],
            )
        else:
            _display_single_job(ans, report_type)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Kill a running job by job ID")
@click.argument("job_id", type=int)
@click.pass_context
def kill(ctx: ClickContext, job_id: int):
    ctx.obj.logger.info(f"Requesting kill for Job [underline blue]#{job_id}[/]..")
    ans = False
    try:
        ans = ctx.obj.kill_running_job(job_id)
        rprint(get_action_status_text(ans, "kill"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "kill"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Delete job by job ID")
@click.argument("job_id", type=int)
@click.pass_context
def rm(ctx: ClickContext, job_id: int):
    ctx.obj.logger.info(f"Requesting delete for Job [underline blue]#{job_id}[/]..")
    ans = False
    try:
        ans = ctx.obj.delete_job_by_id(job_id)
        rprint(get_action_status_text(ans, "delete"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "delete"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Download sample by Job ID")
@click.argument("job_id", type=int)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(exists=False, resolve_path=True),
    required=True,
    help="Name and Path to downloaded analysis sample.",
)
@click.pass_context
def download_sample(ctx: ClickContext, job_id: int, output_file: str):
    ctx.obj.logger.info(
        f"Request sample download from Job [underline blue]#{job_id}[/].."
    )
    ans = False
    try:
        ans = ctx.obj.download_sample(job_id)
        if ans:
            with open(output_file, "wb") as f:
                f.write(ans)

        rprint(get_action_status_text(bool(ans), "download"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(bool(ans), "download"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(
    "poll",
    help="""
    HTTP poll a running job's details until
    it finishes and save result into a file.
    """,
)
@click.argument("job_id", type=int)
@click.option(
    "-t",
    "--max-tries",
    type=int,
    default=5,
    show_default=True,
    help="maximum number of tries",
)
@click.option(
    "-i",
    "--interval",
    type=int,
    default=5,
    show_default=True,
    help="sleep interval between subsequent requests (in sec)",
)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(exists=False, resolve_path=True),
    required=True,
    help="Path to JSON file to save result to",
)
@click.pass_context
def poll(
    ctx: ClickContext, job_id: int, max_tries: int, interval: int, output_file: str
):
    try:
        ans = _poll_for_job_cli(ctx.obj, job_id, max_tries, interval)
        if ans:
            with open(output_file, "w") as fp:
                json.dump(ans, fp, indent=4)
            Console().print(f"Result saved into [u red]{output_file}[/]")
    except Exception as e:
        ctx.obj.logger.fatal(f"Error in retrieving job: {str(e)}")


@jobs.command(help="Kill a running/pending analyzer by name and job ID")
@click.argument("job_id", type=int)
@click.argument("analyzer_name", type=str)
@click.pass_context
def kill_analyzer(ctx: ClickContext, job_id: int, analyzer_name: str):
    ctx.obj.logger.info(
        f"Requesting kill_analyzer for analyzer [underline blue]#{analyzer_name}[/]"
        f" and Job [underline blue]#{job_id}[/].."
    )
    ans = False
    try:
        ans = ctx.obj.kill_analyzer(job_id, analyzer_name)
        rprint(get_action_status_text(ans, "kill"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "kill"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Kill a running/pending connector by name and job ID")
@click.argument("job_id", type=int)
@click.argument("connector_name", type=str)
@click.pass_context
def kill_connector(ctx: ClickContext, job_id: int, connector_name: str):
    ctx.obj.logger.info(
        f"Requesting kill_connector for connector [underline blue]#{connector_name}[/]"
        f" and Job [underline blue]#{job_id}[/].."
    )
    ans = False
    try:
        ans = ctx.obj.kill_connector(job_id, connector_name)
        rprint(get_action_status_text(ans, "kill"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "kill"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Retry a failed/killed analyzer by name and job ID")
@click.argument("job_id", type=int)
@click.argument("analyzer_name", type=str)
@click.pass_context
def retry_analyzer(ctx: ClickContext, job_id: int, analyzer_name: str):
    ctx.obj.logger.info(
        f"Requesting retry_analyzer for analyzer [underline blue]#{analyzer_name}[/]"
        f" and Job [underline blue]#{job_id}[/].."
    )
    ans = False
    try:
        ans = ctx.obj.retry_analyzer(job_id, analyzer_name)
        rprint(get_action_status_text(ans, "retry"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "retry"))
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Retry a failed/killed connector by name and job ID")
@click.argument("job_id", type=int)
@click.argument("connector_name", type=str)
@click.pass_context
def retry_connector(ctx: ClickContext, job_id: int, connector_name: str):
    ctx.obj.logger.info(
        f"Requesting retry_connector for connector [underline blue]#{connector_name}[/]"
        f" and Job [underline blue]#{job_id}[/].."
    )
    ans = False
    try:
        ans = ctx.obj.retry_connector(job_id, connector_name)
        rprint(get_action_status_text(ans, "retry"))
    except IntelOwlClientException as e:
        rprint(get_action_status_text(ans, "retry"))
        ctx.obj.logger.fatal(str(e))
