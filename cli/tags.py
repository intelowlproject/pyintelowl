import click
from rich.console import Console
from rich.table import Table
from rich import box
from pprint import pprint


@click.command(short_help="Manage tags")
@click.option("-a", "--all", is_flag=True, help="List all tags")
@click.option("--id", help="Retrieve tag by ID")
@click.pass_context
def tags(ctx, id, all):
    if all:
        ans, errs = ctx.obj.get_all_tags()
    else:
        if id:
            ans, errs = ctx.obj.get_tag_by_id(id)
    if errs:
        pprint(errs)
    print_table(ans)


def print_table(data):
    console = Console()
    table = Table(show_header=True)
    table.add_column("Id", no_wrap=True, header_style="bold blue")
    table.add_column("Label", no_wrap=True, header_style="bold blue")
    table.add_column("Color", no_wrap=True, header_style="bold blue")
    try:
        for elem in data:
            color = str(elem["color"])
            table.add_row(
                str(elem["id"]),
                str(elem["label"]),
                f"[{color.lower()}]{color}[/{color.lower()}]",
            )
        table.box = box.DOUBLE
        console.print(table, justify="center")
    except Exception as e:
        pprint(e)
