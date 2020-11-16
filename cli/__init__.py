from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import get_analyzer_config
from ._utils import ClickContext

groups = [
    analyse,
    config,
]


cmds = [get_analyzer_config, jobs, tags]


__all__ = [ClickContext, groups, cmds]
