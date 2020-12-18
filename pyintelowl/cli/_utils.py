import click
import logging
import csv
import json
import pathlib
from tinynetrc import Netrc
from rich.emoji import Emoji
from rich.text import Text
from rich.syntax import Syntax
from rich.logging import RichHandler

from pyintelowl import IntelOwl

json_flag_option = [
    click.option(
        "-j",
        "--json",
        "as_json",
        is_flag=True,
        help="output as raw JSON",
    ),
]


class ClickContext(click.Context):
    obj: IntelOwl
    """
    IntelOwl instance
    """


def get_status_text(status: str, as_text=True):
    styles = {
        "pending": ("#CE5C00", str(Emoji("gear"))),
        "running": ("#CE5C00", str(Emoji("gear"))),
        "reported_without_fails": ("#73D216", str(Emoji("heavy_check_mark"))),
        "reported_with_fails": ("#CC0000", str(Emoji("warning"))),
        "failed": ("#CC0000", str(Emoji("cross_mark"))),
    }
    color, emoji = styles[status]
    s = f"[{color}]{status} {emoji}[/]"
    return Text(status + " " + emoji, style=color) if as_text else s


def get_success_text(success):
    success = str(success)
    styles = {
        "True": ("#73D216", str(Emoji("heavy_check_mark"))),
        "False": ("#CC0000", str(Emoji("cross_mark"))),
    }
    color, emoji = styles[success]
    return Text(emoji, style=color)


def get_json_syntax(obj):
    return Syntax(
        json.dumps(obj, indent=2),
        "json",
        theme="ansi_dark",
        word_wrap=True,
        tab_size=2,
    )


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def get_netrc_obj():
    filepath = pathlib.Path().home().joinpath(".netrc")
    filepath.touch(exist_ok=True)
    netrc = Netrc(str(filepath))
    host = netrc["pyintelowl"]
    return netrc, host


def get_tags_str(tags):
    tags_str = ", ".join(
        ["[on {0}]{1}[/]".format(str(t["color"]).lower(), t["label"]) for t in tags]
    )
    return tags_str


def get_logger(level: str = "INFO"):
    fmt = "%(message)s"
    logging.basicConfig(
        level=level, format=fmt, datefmt="[%X]", handlers=[RichHandler(markup=True)]
    )
    logger = logging.getLogger("rich")
    return logger


def get_json_data(filepath):
    obj = None
    with open(filepath) as _tmp:
        line = _tmp.readline()
        if line[0] in "[{":
            with open(filepath) as fp:
                obj = json.load(fp)
        else:
            with open(filepath) as fp:
                reader = csv.DictReader(fp)
                obj = [dict(row) for row in reader]
    return obj


def get_version_number() -> str:
    from .. import version

    return version.__version__
