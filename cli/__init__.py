from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import get_analyzer_config

groups = [
    analyse,
    jobs,
    tags,
    config,
]

cmds = [get_analyzer_config]

__all__ = [groups, cmds]
