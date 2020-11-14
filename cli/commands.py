import click


@click.command(
    short_help="Get current state of `analyzer_config.json` from the IntelOwl instance"
)
@click.pass_context
def get_analyzer_config(ctx):
    res = ctx.obj.get_analyzer_configs()
    print(res)
