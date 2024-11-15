from .analyse import analyse
from .commands import analyzer_healthcheck, connector_healthcheck
from .config import config
from .investigations import investigations
from .jobs import jobs
from .playbooks import playbooks
from .tags import tags

groups = [
    analyse,
    config,
    jobs,
    tags,
    playbooks,
    investigations,
]

cmds = [
    analyzer_healthcheck,
    connector_healthcheck,
]
