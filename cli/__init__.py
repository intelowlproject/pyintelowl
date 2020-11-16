from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import get_analyzer_config
from ._utils import ClickContext

groups = [
    analyse,
    tags,
    config,
]

cmds = [get_analyzer_config, jobs]

__all__ = [ClickContext, groups, cmds]
