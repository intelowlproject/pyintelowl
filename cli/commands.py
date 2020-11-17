import click
from ._utils import ClickContext, get_success_text, get_json_syntax
from rich.console import Console
from rich.table import Table
from rich import box, print as rprint
from fnmatch import filter


@click.command(
    "gac",
    short_help="Get current state of `analyzer_config.json` from the IntelOwl instance",
)
@click.option(
    "-m", "--re-match", default="*", help="Pattern/Name of Required Analyzer(s)"
)
@click.option("-j", "--json", is_flag=True, help="Just Pretty prints json data")
@click.pass_context
def get_analyzer_config(ctx: ClickContext, json, re_match):
    raw, err = ctx.obj.get_analyzer_configs()
    filtered_analyzers = filter(raw.keys(), re_match)
    res = {key: raw[key] for key in filtered_analyzers}

    if err:
        print(err)
    else:
        if json:
            rprint(res)
        else:
            console = Console()
            headers = [
                "Name",
                "Type",
                "Description",
                "Supported\nTypes",
                "External\nService",
                "Leaks\nInfo",
                "Requires\nConfig",
                "Additional\nConfig",
            ]
            header_style = "bold blue"
            with console.pager(styles=True):
                table = Table(
                    show_header=True,
                    title="Analyser Configurations",
                    box=box.DOUBLE_EDGE,
                    show_lines=True,
                )
                for h in headers:
                    table.add_column(h, header_style=header_style, justify="center")
                for name in res.keys():
                    table.add_row(
                        name,
                        res[name]["type"],
                        res[name].get("description", ""),
                        get_json_syntax(
                            res[name].get(
                                "observable_supported",
                                res[name].get("supported_filetypes", ""),
                            )
                        ),
                        get_success_text(res[name].get("external_service", False)),
                        get_success_text(res[name].get("leaks_info", False)),
                        get_success_text(
                            res[name].get("requires_configuration", False)
                        ),
                        get_json_syntax(res[name].get("additional_config_params", {})),
                    )
                console.print(table)
