import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box, print
from json import dumps as json_dumps

from ._utils import ClickContext, get_status_text


@click.command(short_help="Info about Jobs")
@click.option("-a", "--all", is_flag=True, help="List all jobs")
@click.option("--id", help="Retrieve Job details by ID")
@click.pass_context
def jobs(ctx: ClickContext, id, all):
    """
    List jobs
    """
    if all:
        res = ctx.obj.get_all_jobs()
        display_all_jobs(res["answer"])
    elif id:
        res = ctx.obj.get_job_by_id(id)
        display_single_job(res["answer"])


def display_single_job(data):
    console = Console()
    style = "bold #31DDCF"
    console.print(Text("Id: ", style=style, end=""), Text(str(data["id"])))
    tags = ", ".join([t["label"] for t in data["tags"]])
    console.print(Text("Tags: ", style=style, end=""), Text(tags))
    console.print(Text("User: ", style=style, end=""), Text(data["source"]))
    console.print(Text("MD5: ", style=style, end=""), Text(data["md5"]))
    console.print(
        Text("Name: ", style=style, end=""),
        Text(data["observable_name"] if data["observable_name"] else data["file_name"]),
    )
    console.print(
        Text("Classification: ", style=style, end=""),
        Text(
            data["observable_classification"]
            if data["observable_classification"]
            else data["file_mimetype"]
        ),
    )
    console.print(
        Text("Status: ", style=style, end=""), get_status_text(data["status"])
    )

    table = Table(show_header=True)
    headers = ["Name", "Errors", "Report", "Status"]
    for h in headers:
        table.add_column(h, header_style="bold blue")

    for element in data["analysis_reports"]:
        table.add_row(
            element["name"],
            json_dumps(element["errors"], indent=2),
            json_dumps(element["report"], indent=2),
            str(element["success"]),
        )
    console.print(table)


def display_all_jobs(data):
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
        print(e)
