import click
from pyintelowl.pyintelowl import IntelOwl


class ClickContext(click.Context):
    obj: IntelOwl
    """
    IntelOwl instance
    """


def get_status_text(status: str):
    from rich.emoji import Emoji
    from rich.text import Text
    styles = {
        "pending": ("#CE5C00", str(Emoji("gear"))),
        "running": ("#CE5C00", str(Emoji("gear"))),
        "reported_without_fails": ("#73D216", str(Emoji("heavy_check_mark"))),
        "reported_with_fails": ("#CC0000", str(Emoji("warning"))),
        "failed": ("#CC0000", str(Emoji("cross_mark"))),
    }
    col, emoji = styles[status]
    return Text(status + " " + emoji, style=col)


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options
