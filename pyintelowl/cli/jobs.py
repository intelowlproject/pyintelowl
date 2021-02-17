import click
import json
from rich import print as rprint
from rich.console import Console
from pyintelowl.exceptions import IntelOwlClientException
from ..cli._utils import (
    ClickContext,
    add_options,
    json_flag_option,
    get_action_status_text,
)
from ..cli._jobs_utils import (
    _display_all_jobs,
    _display_single_job,
    _result_filter_and_tabular_print,
    _poll_for_job_cli,
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
        if status:
            ans = [el for el in ans if el["status"].lower() == status.lower()]
        if as_json:
            rprint(json.dumps(ans, indent=4))
        else:
            _display_all_jobs(ctx.obj.logger, ans)
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@jobs.command(help="Tabular print job attributes and results for a job ID")
@click.argument("job_id", type=int)
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
def view(ctx: ClickContext, job_id: int, categorize: bool, as_json: bool):
    ctx.obj.logger.info(f"Requesting Job [underline blue]#{job_id}[/]..")
    if as_json and categorize:
        raise click.Abort("Cannot use the -c and -j options together")
    try:
        ans = ctx.obj.get_job_by_id(job_id)
        if as_json:
            rprint(json.dumps(ans, indent=4))
        elif categorize:
            if ans["is_sample"]:
                raise click.Abort("Cannot use the -c option for a file analysis")
            _result_filter_and_tabular_print(
                ans["analysis_reports"],
                ans["observable_name"],
                ans["observable_classification"],
            )
        else:
            _display_single_job(ans)
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
