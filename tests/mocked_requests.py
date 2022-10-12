from tests.utils import ROOT_DIR, TEST_FILE, MockResponse, get_file_data


def mocked_raise_exception(*args, **kwargs):
    raise Exception


def mocked_analyzer_config(*args, **kwargs):
    return MockResponse(
        {
            "test_analyzer": {
                "type": "observable",
                "python_module": "test_class.test_module",
                "description": "a test analyzer",
                "disabled": False,
                "external_service": False,
                "leaks_info": False,
                "observable_supported": ["domain"],
                "config": {"soft_time_limit": 30, "queue": "default"},
                "secrets": {},
            }
        },
        200,
        "/api/get_analyzer_configs",
    )


def mocked_connector_config(*args, **kwargs):
    return MockResponse(
        {
            "test_connector": {
                "python_module": "test_class.test_module",
                "description": "a test connector",
                "disabled": False,
                "maximum_tlp": "WHITE",
                "config": {"soft_time_limit": 30, "queue": "default"},
                "secrets": {},
            }
        },
        200,
        "/api/get_connector_configs",
    )


def mocked_playbook_config(*args, **kwargs):
    return MockResponse(
        {
            "test_playbook": {
                "name": "test_playbook",
                "supports": ["ip", "url", "domain", "generic", "hash"],
                "python_module": "",
                "disabled": False,
                "description": "a test playbook",
                "analyzers": {
                    "Classic_DNS": {
                        "query_type": "A",
                    },
                },
                "connectors": {},
                "verification": {},
            }
        },
        200,
        "/api/get_playbook_configs",
    )


def mocked_ask_analysis_success(*args, **kwargs):
    return MockResponse(
        {
            "job_id": 1,
            "status": "running",
            "analyzers_to_execute": ["test_1", "test_2"],
        },
        200,
        "/api/ask_analysis_availability",
    )


def mocked_ask_analysis_no_status(*args, **kwargs):
    return MockResponse(
        {
            "job_id": 1,
        },
        200,
        "/api/ask_analysis_availability",
    )


def mocked_send_analysis_success(*args, **kwargs):
    return MockResponse(
        {
            "status": "accepted",
            "job_id": 1,
            "warnings": [],
            "analyzers_running": ["test_1", "test_2"],
        },
        200,
        "/api/analyze_observable",
    )


def mocked_send_playbook_analysis_success(*args, **kwargs):
    return MockResponse(
        {
            "count": 1,
            "results": [
                {
                    "job_id": 266,
                    "status": "accepted",
                    "warnings": [],
                    "analyzers_running": [
                        "TEST_ANALYZER",
                    ],
                    "connectors_running": [],
                    "playbooks_running": ["FREE_PLAYBOOK"],
                }
            ],
        },
        200,
        "/api/playbook/analyze_multiple_observables",
    )


def mocked_ask_analysis_no_job_id(*args, **kwargs):
    return MockResponse(
        {
            "status": "running",
        },
        200,
        "/api/ask_analysis_availability",
    )


def mocked_get_job_by_id(*args, **kwargs):
    return MockResponse(
        {
            "id": 1,
            "tags": [],
            "source": "test-user",
            "md5": "test-md5-hash",
            "observable_name": "test-observable_name",
            "observable_classification": "test",
            "status": "reported_without_fails",
            "analyzer_reports": [
                {
                    "name": "test-analyzer",
                    "errors": [],
                    "report": {},
                    "status": "SUCCESS",
                }
            ],
        },
        200,
        "/api/jobs/1",
    )


def mocked_get_all_jobs(*args, **kwargs):
    return MockResponse(
        {"count": 1, "total_pages": 1, "results": []},
        200,
        "/api/jobs",
    )


def mocked_delete_job_by_id(*args, **kwargs):
    return MockResponse(
        True,
        200,
        "/api/jobs/1",
    )


def mocked_kill_job(*args, **kwargs):
    return MockResponse(
        True,
        204,
        "/api/jobs/1/kill",
    )


def mocked_kill_analyzer(*args, **kwargs):
    return MockResponse(
        True,
        204,
        "/api/jobs/1/analyzer/MISP/kill",
    )


def mocked_kill_connector(*args, **kwargs):
    return MockResponse(
        True,
        204,
        "/api/jobs/1/connector/MISP/kill",
    )


def mocked_retry_analyzer(*args, **kwargs):
    return MockResponse(
        True,
        204,
        "/api/jobs/1/analyzer/MISP/retry",
    )


def mocked_retry_connector(*args, **kwargs):
    return MockResponse(
        True,
        204,
        "/api/jobs/1/connector/MISP/retry",
    )


def mocked_analyzer_healthcheck(*args, **kwargs):
    return MockResponse(
        {"status": True},
        200,
        "/api/analyzer/MISP/healthcheck",
    )


def mocked_connector_healthcheck(*args, **kwargs):
    return MockResponse(
        {"status": True},
        200,
        "/api/connector/MISP/healthcheck",
    )


def mocked_download_job_sample(*args, **kwargs):
    return MockResponse(
        {},
        200,
        "/api/jobs/1/download_sample",
        content=get_file_data(f"{ROOT_DIR}/tests/test_files/{TEST_FILE}"),
    )


def mocked_get_tag_by_id(*args, **kwargs):
    return MockResponse(
        {"id": 1, "label": "test-tag", "color": "green"},
        200,
        "/api/tag/1",
    )


def mocked_get_all_tags(*args, **kwargs):
    return MockResponse(
        [],
        200,
        "/api/tags",
    )


def mocked_create_tag(*args, **kwargs):
    return MockResponse(
        {"id": 1, "label": "test-tag", "color": "white"},
        200,
        "/api/tags",
    )


def mocked_edit_tag(*args, **kwargs):
    return MockResponse(
        {"id": 1, "label": "modified-test-tag", "color": "black"},
        200,
        "/api/tags/1",
    )


def mocked_delete_tag_by_id(*args, **kwargs):
    return MockResponse(
        True,
        200,
        "/api/tags/1",
    )
