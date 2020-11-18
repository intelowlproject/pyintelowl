import click
import click_spinner
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import RenderGroup
from rich import box, print as rprint

from pyintelowl.exceptions import IntelOwlAPIException
from ._utils import (
    ClickContext,
    get_status_text,
    get_success_text,
    get_json_syntax,
    get_tags_str,
)


@click.group("jobs", short_help="Manage Jobs", invoke_without_command=True)
@click.option("-a", "--all", is_flag=True, help="List all jobs")
@click.option("--id", type=int, default=0, help="Retrieve Job details by ID")
@click.option(
    "--status", type=str, help="List jobs with given status (Only use with --all)"
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
                ans = [el for el in ans if el["status"] == status]

            _display_all_jobs(ans)
        elif id:
            ctx.obj.logger.info(f"Requesting Job [underline blue]#{id}[/]..")
            with click_spinner.spinner():
                ans = ctx.obj.get_job_by_id(id)
            _display_single_job(ans)
        else:
            click.echo(ctx.get_usage())
    except IntelOwlAPIException as e:
        ctx.obj.logger.fatal(str(e))


@jobs.command("poll", short_help="HTTP poll a currently running job's details")
@click.option(
    "-t",
    "--max-tries",
    type=int,
    default=0,
    show_default=True,
    help="maximum number of tries (in sec)",
)
@click.option(
    "-i",
    "--interval",
    type=int,
    default=5,
    show_default=True,
    help="sleep interval before subsequent requests (in sec)",
)
@click.pass_context
def poll(ctx: ClickContext, max_tries: int, interval: int):
    pass


def _display_single_job(data):
    console = Console()
    style = "[bold #31DDCF]"
    headers = ["Name", "Status", "Report", "Errors"]
    with console.pager(styles=True):
        # print job attributes
        tags = get_tags_str(data["tags"])
        status = get_status_text(data["status"])
        name = data["observable_name"] if data["observable_name"] else data["file_name"]
        clsfn = (
            data["observable_classification"]
            if data["observable_classification"]
            else data["file_mimetype"]
        )
        r = RenderGroup(
            f"{style}Job ID:[/] {str(data['id'])}",
            f"{style}User:[/] {data['source']}",
            f"{style}MD5:[/] {data['md5']}",
            f"{style}Name:[/] {name}",
            f"{style}Classification:[/] {clsfn}",
            f"{style}Tags:[/] {tags}",
            f"{style}Status:[/] {status}",
        )
        console.print(Panel(r, title="Job attributes"))

        # construct job analysis table

        table = Table(
            show_header=True,
            title="Analysis Data",
            box=box.DOUBLE_EDGE,
            show_lines=True,
        )
        # add headers
        for h in headers:
            table.add_column(h, header_style="bold blue")
        # add rows
        for el in data["analysis_reports"]:
            table.add_row(
                el["name"],
                get_success_text((el["success"])),
                get_json_syntax(el["report"]) if el["report"] else None,
                get_json_syntax(el["errors"]) if el["errors"] else None,
            )
        console.print(table)


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
