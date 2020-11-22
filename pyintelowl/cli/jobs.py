import time
import click
import click_spinner
from rich.console import Console
from rich.table import Table
from rich import box, print as rprint
from rich.progress import track
from pyintelowl.exceptions import IntelOwlClientException
from ..cli._utils import ClickContext, get_status_text
from ..cli._jobs_utils import (
    _display_single_job,
    _render_job_attributes,
    _render_job_analysis_table,
)


@click.group("jobs", help="Manage Jobs", invoke_without_command=True)
@click.option("-a", "--all", is_flag=True, help="List all jobs")
@click.option("--id", type=int, default=0, help="Retrieve Job details by ID")
@click.option(
    "--status",
    type=click.Choice(
        [
            "pending",
            "running",
            "reported_without_fails",
            "reported_with_fails",
            "failed",
        ],
        case_sensitive=False,
    ),
    show_choices=True,
    help="Filter jobs with a particular status. Should be used with --all.",
)
@click.pass_context
def jobs(ctx: ClickContext, id: int, all: bool, status: str):
    """
    Manage Jobs
    """
    try:
        if all:
            ctx.obj.logger.info("Requesting list of jobs..")
            with click_spinner.spinner():
                ans = ctx.obj.get_all_jobs()
            if status:
                ans = [el for el in ans if el["status"].lower() == status.lower()]
            _display_all_jobs(ans)
        elif id:
            ctx.obj.logger.info(f"Requesting Job [underline blue]#{id}[/]..")
            with click_spinner.spinner():
                ans = ctx.obj.get_job_by_id(id)
            _display_single_job(ans)
        else:
            if not ctx.invoked_subcommand:
                click.echo(ctx.get_usage())
    except IntelOwlClientException as e:
        ctx.obj.logger.fatal(str(e))


@jobs.command("poll", help="HTTP poll a currently running job's details")
@click.option("--id", type=int, required=True, help="HTTP poll a job for live updates")
@click.option(
    "-t",
    "--max-tries",
    type=int,
    default=0,
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
@click.pass_context
def poll(ctx: ClickContext, id: int, max_tries: int, interval: int):
    console = Console()
    try:
        for i in track(
            range(max_tries),
            description=f"Polling Job [underline blue]#{id}[/]..",
            console=console,
        ):
            if i != 0:
                console.print(f"sleeping for {interval} seconds before next request..")
                time.sleep(interval)
            ans = ctx.obj.get_job_by_id(id)
            status = ans["status"].lower()
            if i == 0:
                console.print(_render_job_attributes(ans))
            if status not in ["running", "pending"]:
                console.print(
                    "\nPolling stopped because job has finished with status: ",
                    get_status_text(status),
                    end="",
                )
                break
            console.clear()
            console.print(
                _render_job_analysis_table(ans["analysis_reports"], verbose=False),
                justify="center",
            )
        view_full = click.prompt(
            "Would you like to view full result ? [y/N]: ",
            type=bool,
        )
        if view_full:
            _display_single_job(ans)
    except Exception as e:
        ctx.obj.logger.error(f"Error in retrieving job: {str(e)}")


def _display_all_jobs(data):
    console = Console()
    table = Table(show_header=True, title="List of Jobs", box=box.DOUBLE_EDGE)
    header_style = "bold blue"
    table.add_column(header="Id", header_style=header_style)
    table.add_column(header="Name", header_style=header_style)
    table.add_column(header="Type", header_style=header_style)
    table.add_column(header="Tags", header_style=header_style)
    table.add_column(
        header="Analyzers\nCalled", justify="center", header_style=header_style
    )
    table.add_column(
        header="Process\nTime(s)", justify="center", header_style=header_style
    )
    table.add_column(header="Status", header_style=header_style)
    try:
        for el in data:
            table.add_row(
                str(el["id"]),
                el["observable_name"] if el["observable_name"] else el["file_name"],
                el["observable_classification"]
                if el["observable_classification"]
                else el["file_mimetype"],
                ", ".join([t["label"] for t in el["tags"]]),
                el["no_of_analyzers_executed"],
                str(el["process_time"]),
                get_status_text(el["status"]),
            )
        console.print(table, justify="center")
    except Exception as e:
        rprint(e)
