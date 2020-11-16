import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from json import dumps as json_dumps
from pprint import pprint


@click.command(short_help="Manage jobs")
@click.option("-a", "--all", is_flag=True, help="List all jobs")
@click.option("--id", help="Retrieve Job details by ID")
@click.pass_context
def jobs(ctx, id, all):
    """
    List jobs
    """
    if all:
        errors, answer = ctx.obj.get_all_jobs()
        if not errors:
            display_all_jobs(answer)
        else:
            pprint(errors)
    elif id:
        errors, answer = ctx.obj.get_job_by_id(id)
        if not errors:
            display_single_job(answer)
        else:
            pprint(errors)


def display_single_job(data):
    console = Console()
    style = "bold  #31DDCF"
    try:
        console.print(Text("Id: ", style=style, end=""), Text(str(data["id"])))
        console.print(
            Text("Tags: ", style=style, end=""), Text(", ".join(data["tags"]))
        )
        console.print(Text("User: ", style=style, end=""), Text(data["source"]))
        console.print(Text("MD5: ", style=style, end=""), Text(data["md5"]))
        console.print(
            Text("Name: ", style=style, end=""),
            Text(
                data["observable_name"]
                if data["observable_name"]
                else data["file_name"]
            ),
        )
        console.print(
            Text("Classification: ", style=style, end=""),
            Text(
                data["observable_classification"]
                if data["observable_classification"]
                else data["file_mimetype"]
            ),
        )
        console.print(Text("Status: ", style=style, end=""), job_status(data["status"]))

        header_style = "bold blue"
        table = Table(show_header=True)
        table.add_column("Name", header_style=header_style)
        table.add_column("Errors", header_style=header_style)
        table.add_column("Report", header_style=header_style)
        table.add_column("Status", header_style=header_style)

        for element in data["analysis_reports"]:
            table.add_row(
                element["name"],
                json_dumps(element["errors"], indent=2),
                json_dumps(element["report"], indent=2),
                str(element["success"]),
            )
        console.print(table)
    except Exception:
        pprint(data)  # Mostly It contains the reason for error


def job_status(status):
    styles = {
        "pending": "#CE5C00",
        "running": "#CE5C00",
        "reported_without_fails": "#73D216",
        "reported_with_fails": "#CC0000",
        "failed": "#CC0000",
    }
    return Text(status, style=styles[status])


def display_all_jobs(data):
    console = Console()
    table = Table(show_header=True)
    header_style = "bold blue"
    table.add_column(header="Id", header_style=header_style)
    table.add_column(header="Name", header_style=header_style)
    table.add_column(header="Type", header_style=header_style)
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
                element["no_of_analyzers_executed"],
                str(element["process_time"]),
                job_status(element["status"]),
            )
            table.box = box.DOUBLE
        console.print(table, justify="center")
    except Exception as e:
        print(e)
