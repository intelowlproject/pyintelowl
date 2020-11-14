import click


@click.group("tags", invoke_without_command=True)
def tags():
    """
    List tags
    """
    pass
