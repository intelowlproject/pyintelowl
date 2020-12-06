import time
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.console import RenderGroup, Console
from ..cli._utils import (
    get_status_text,
    get_success_text,
    get_tags_str,
    get_json_syntax,
)
from pyintelowl.exceptions import IntelOwlClientException
from ..cli.domain_checkers import Checkers, console as checkers_console


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


def _display_all_jobs(logger, rows):
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
        for el in rows:
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
        logger.fatal(e)


def _result_filter_and_tabular_print(result, observable: str, obs_clsfn: str):
    checkers = Checkers(result, observable)
    func = checkers.func_map.get(obs_clsfn, None)
    if not func:
        raise IntelOwlClientException(f"Not supported observable type: {obs_clsfn}")
    with checkers_console.pager():
        func()


def _poll_for_job_cli(
    obj,
    job_id: int,
    max_tries=5,
    interval=5,
):
    console = Console()
    ans = None
    for i in track(
        range(max_tries),
        description=f"Polling Job [underline blue]#{job_id}[/]..",
        console=console,
        transient=True,
        update_period=interval,
    ):
        if i != 0:
            # console.print(f"sleeping for {interval} seconds before next request..")
            time.sleep(interval)
        ans = obj.get_job_by_id(job_id)
        status = ans["status"].lower()
        if i == 0:
            console.print(_render_job_attributes(ans))
        console.print(
            _render_job_analysis_table(ans["analysis_reports"], verbose=False),
            justify="center",
        )
        if status not in ["running", "pending"]:
            console.print(
                "\nPolling stopped because job has finished with status: ",
                get_status_text(status),
                end="",
            )
            break
    return ans
