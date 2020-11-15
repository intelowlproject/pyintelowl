from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import get_analyzer_config

groups = [
    analyse,
    jobs,
    config,
]

cmds = [get_analyzer_config, tags]

__all__ = [groups, cmds]
