import click


@click.group("config", invoke_without_command=True)
@click.pass_context
def config():
    """
    Set or view config variables
    """
    pass
