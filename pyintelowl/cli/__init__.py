from .analyse import analyse
from .jobs import jobs
from .tags import tags
from .config import config
from .commands import (
    analyzer_healthcheck,
    connector_healthcheck,
    get_analyzer_config,
    get_connector_config,
)

groups = [
    analyse,
    config,
    jobs,
    tags,
]


cmds = [
    get_analyzer_config,
    get_connector_config,
    analyzer_healthcheck,
    connector_healthcheck,
]
