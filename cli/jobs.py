import click
import click_spinner
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box, print as rprint

from ._utils import ClickContext, get_status_text, get_success_text, get_json_syntax


@click.group("jobs", short_help="Manage Jobs", invoke_without_command=True)
@click.option("-a", "--all", is_flag=True, help="List all jobs")
@click.option("--id", type=int, default=0, help="Retrieve Job details by ID")
@click.pass_context
def jobs(ctx: ClickContext, id: int, all: bool):
    """
    Manage Jobs
    """
    errs = None
    if all:
        with click_spinner.spinner():
            ans, errs = ctx.obj.get_all_jobs()
        if not errs:
            _display_all_jobs(ans)
    elif id:
        with click_spinner.spinner():
            ans, errs = ctx.obj.get_job_by_id(id)
        if not errs:
            _display_single_job(ans)
    else:
        print("Use -h or --help for help.")
    if errs:
        rprint(errs)


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
    style = "bold #31DDCF"
    headers = ["Name", "Status", "Report", "Errors"]
    with console.pager(styles=True):
        # print job attributes
        console.print(Text("Id: ", style=style, end=""), Text(str(data["id"])))
        tags = ", ".join([t["label"] for t in data["tags"]])
        console.print(Text("Tags: ", style=style, end=""), Text(tags))
        console.print(Text("User: ", style=style, end=""), Text(data["source"]))
        console.print(Text("MD5: ", style=style, end=""), Text(data["md5"]))
        console.print(
            Text("Name: ", style=style, end=""),
            (data["observable_name"] if data["observable_name"] else data["file_name"]),
        )
        console.print(
            Text("Classification: ", style=style, end=""),
            (
                data["observable_classification"]
                if data["observable_classification"]
                else data["file_mimetype"]
            ),
        )
        console.print(
            Text("Status: ", style=style, end=""), get_status_text(data["status"])
        )

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
        for element in data["analysis_reports"]:
            table.add_row(
                element["name"],
                get_success_text((element["success"])),
                get_json_syntax(element["report"]) if element["report"] else None,
                get_json_syntax(element["errors"]) if element["errors"] else None,
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
        for element in data:
            table.add_row(
                str(element["id"]),
                element["observable_name"],
                element["observable_classification"],
                ", ".join([t["label"] for t in element["tags"]]),
                element["no_of_analyzers_executed"],
                str(element["process_time"]),
                get_status_text(element["status"]),
            )
        console.print(table, justify="center")
    except Exception as e:
        rprint(e)
