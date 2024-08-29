from .analyse import analyse
from .commands import analyzer_healthcheck, connector_healthcheck
from .config import config
from .jobs import jobs
from .tags import tags

groups = [
    analyse,
    config,
    jobs,
    tags,
]


cmds = [
    analyzer_healthcheck,
    connector_healthcheck,
]
