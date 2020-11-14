import click


@click.group("jobs", invoke_without_command=True)
def jobs():
    """
    List jobs
    """
    pass


@jobs.command(short_help="HTTP Poll for a job who's status is `running`")
def poll():
    pass
