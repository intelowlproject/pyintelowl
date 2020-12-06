from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import get_analyzer_config

groups = [
    analyse,
    config,
    jobs,
    tags,
]


cmds = [get_analyzer_config]
