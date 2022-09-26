from .analyse import analyse
from .commands import (
    analyzer_healthcheck,
    connector_healthcheck,
    get_analyzer_config,
    get_connector_config,
    get_playbook_config,
)
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
    get_analyzer_config,
    get_connector_config,
    get_playbook_config,
    analyzer_healthcheck,
    connector_healthcheck,
]
