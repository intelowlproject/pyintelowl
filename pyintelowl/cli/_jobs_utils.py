from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.console import RenderGroup, Console
from ..cli._utils import (
    get_status_text,
    get_success_text,
    get_tags_str,
    get_json_syntax,
)


def _display_single_job(data):
    console = Console()
    with console.pager(styles=True):
        # print job attributes
        attrs = _render_job_attributes(data)
        console.print(attrs)
        # construct job analysis table
        table = _render_job_analysis_table(data["analysis_reports"], verbose=True)
        console.print(table, justify="center")


def _render_job_analysis_table(rows, verbose=False):
    if verbose:
        headers = ["Name", "Status", "Report", "Errors"]
    else:
        headers = ["Name", "Status"]
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
    for el in rows:
        cols = [
            el["name"],
            get_success_text((el["success"])),
        ]
        if verbose:
            cols.append(get_json_syntax(el["report"]) if el["report"] else None)
            cols.append(get_json_syntax(el["errors"]) if el["errors"] else None)
        table.add_row(*cols)
    return table


def _render_job_attributes(data):
    style = "[bold #31DDCF]"
    tags = get_tags_str(data["tags"])
    name = data["observable_name"] if data["observable_name"] else data["file_name"]
    clsfn = (
        data["observable_classification"]
        if data["observable_classification"]
        else data["file_mimetype"]
    )
    status: str = get_status_text(data["status"], as_text=False)
    r = RenderGroup(
        f"{style}Job ID:[/] {str(data['id'])}",
        f"{style}User:[/] {data['source']}",
        f"{style}MD5:[/] {data['md5']}",
        f"{style}Name:[/] {name}",
        f"{style}Classification:[/] {clsfn}",
        f"{style}Tags:[/] {tags}",
        f"{style}Status:[/] {status}",
    )
    return Panel(r, title="Job attributes")
