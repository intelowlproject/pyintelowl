from tests.utils import ROOT_DIR, TEST_FILE, MockResponse, get_file_data


def mocked_raise_exception(*args, **kwargs):
    raise Exception


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


def mocked_get_investigation_by_id(*args, **kwargs):
    return MockResponse(
        {
            "id": 1,
            "tags": [],
            "tlp": "CLEAR",
            "total_jobs": 2,
            "jobs": [1],
            "status": "concluded",
            "for_organization": True,
            "name": "Analyzer1: https://www.test.com",
            "description": "test_description",
            "start_time": "2024-11-13T07:42:17.534614Z",
            "end_time": "2024-11-13T07:42:35.861687Z",
            "owner": "admin",
        },
        200,
        "/api/investigation/1",
    )


def mocked_get_investigation_tree_by_id(*args, **kwargs):
    return MockResponse(
        {
            "name": "InvestigationName: https://www.test.com",
            "owner": 1,
            "jobs": [
                {
                    "pk": 1,
                    "analyzed_object_name": "https://www.test.com",
                    "playbook": "Playbook1",
                    "status": "reported_without_fails",
                    "received_request_time": "2024-11-13T07:42:17.534614Z",
                    "is_sample": False,
                    "children": [
                        {
                            "pk": 2,
                            "analyzed_object_name": "test.0",
                            "pivot_config": "Pivot1",
                            "playbook": "Playbook2",
                            "status": "reported_without_fails",
                            "received_request_time": "2024-11-13T07:42:35.243833Z",
                            "is_sample": True,
                        }
                    ],
                }
            ],
        },
        200,
        "/api/investigation/1/tree",
    )


def mocked_delete_job_from_investigation(*args, **kwargs):
    return MockResponse(
        {
            "id": 1,
            "tags": [],
            "tlp": "CLEAR",
            "total_jobs": 1,
            "jobs": [2],
            "status": "concluded",
            "for_organization": True,
            "name": "InvestigationName: https://www.test.com",
            "description": "",
            "start_time": "2024-11-14T10:38:05.459358Z",
            "end_time": "2024-11-14T10:38:17.638776Z",
            "owner": "admin",
        },
        200,
        "/api/investigation/1/remove_job",
    )


def mocked_add_job_to_investigation(*args, **kwargs):
    return MockResponse(
        {
            "id": 1,
            "tags": [],
            "tlp": "CLEAR",
            "total_jobs": 2,
            "jobs": [2],
            "status": "concluded",
            "for_organization": True,
            "name": "InvestigationName: https://www.test.com",
            "description": "",
            "start_time": "2024-11-14T10:38:05.459358Z",
            "end_time": "2024-11-14T10:38:17.638776Z",
            "owner": "admin",
        },
        200,
        "/api/investigation/1/add_job",
    )


def mocked_get_investigation_tree_by_id_two_results(*args, **kwargs):
    return MockResponse(
        {
            "name": "InvestigationName: https://www.test.com",
            "owner": 1,
            "jobs": [
                {
                    "pk": 1,
                    "analyzed_object_name": "https://www.test.com",
                    "playbook": "Playbook1",
                    "status": "reported_without_fails",
                    "received_request_time": "2024-11-13T07:42:17.534614Z",
                    "is_sample": False,
                },
                {
                    "pk": 2,
                    "analyzed_object_name": "https://www.test2.com",
                    "playbook": "Playbook2",
                    "status": "reported_without_fails",
                    "received_request_time": "2024-11-14T10:38:05.459358Z",
                    "is_sample": False,
                },
            ],
        },
        200,
        "/api/investigation/1/tree",
    )


def mocked_get_investigation_tree_by_id_one_result(*args, **kwargs):
    return MockResponse(
        {
            "name": "InvestigationName: https://www.test.com",
            "owner": 1,
            "jobs": [
                {
                    "pk": 2,
                    "analyzed_object_name": "https://www.test2.com",
                    "playbook": "Playbook2",
                    "status": "reported_without_fails",
                    "received_request_time": "2024-11-14T10:38:05.459358Z",
                    "is_sample": False,
                },
            ],
        },
        200,
        "/api/investigation/1/tree",
    )


def mocked_get_all_investigations(*args, **kwargs):
    return MockResponse(
        {
            "count": 2,
            "total_pages": 1,
            "results": [
                {
                    "id": 2,
                    "tags": [],
                    "tlp": "CLEAR",
                    "total_jobs": 2,
                    "jobs": [2],
                    "status": "concluded",
                    "for_organization": True,
                    "name": "investigation2",
                    "description": "",
                    "start_time": "2024-11-13T07:42:17.534614Z",
                    "end_time": "2024-11-13T07:42:35.861687Z",
                    "owner": "admin",
                },
                {
                    "id": 1,
                    "tags": [],
                    "tlp": "CLEAR",
                    "total_jobs": 2,
                    "jobs": [1],
                    "status": "concluded",
                    "for_organization": True,
                    "name": "investigation1",
                    "description": "",
                    "start_time": "2024-11-12T11:10:42.887446Z",
                    "end_time": "2024-11-12T11:10:49.632430Z",
                    "owner": "admin",
                },
            ],
        },
        200,
        "/api/investigation",
    )


def mocked_get_playbook_by_name(*args, **kwargs):
    return MockResponse(
        {
            "id": 1,
            "type": ["test"],
            "analyzers": ["Analyzer1"],
            "connectors": [],
            "pivots": [],
            "visualizers": [],
            "runtime_configuration": {
                "pivots": {},
                "analyzers": {},
                "connectors": {},
                "visualizers": {},
            },
            "scan_mode": 2,
            "scan_check_time": "1:00:00:00",
            "tags": [],
            "tlp": "CLEAR",
            "weight": 1,
            "is_editable": False,
            "for_organization": False,
            "name": "Playbook1",
            "description": "test",
            "disabled": False,
            "starting": True,
            "owner": None,
        },
        200,
        "/api/playbook/Playbook1",
    )


def mocked_get_all_playbooks(*args, **kwargs):
    return MockResponse(
        {
            "count": 2,
            "total_pages": 1,
            "results": [
                {
                    "id": 1,
                    "type": ["test"],
                    "analyzers": ["Analyzer1"],
                    "connectors": [],
                    "pivots": [],
                    "visualizers": [],
                    "runtime_configuration": {
                        "pivots": {},
                        "analyzers": {},
                        "connectors": {},
                        "visualizers": {},
                    },
                    "scan_mode": 2,
                    "scan_check_time": "1:00:00:00",
                    "tags": [],
                    "tlp": "CLEAR",
                    "weight": 1,
                    "is_editable": False,
                    "for_organization": False,
                    "name": "Playbook1",
                    "description": "test",
                    "disabled": False,
                    "starting": True,
                    "owner": None,
                },
                {
                    "id": 2,
                    "type": ["test2"],
                    "analyzers": ["Analyzer2"],
                    "connectors": [],
                    "pivots": ["Pivot1"],
                    "visualizers": ["Visualizer"],
                    "runtime_configuration": {
                        "pivots": {},
                        "analyzers": {},
                        "connectors": {},
                        "visualizers": {},
                    },
                    "scan_mode": 2,
                    "scan_check_time": "1:00:00:00",
                    "tags": [],
                    "tlp": "AMBER",
                    "weight": 1,
                    "is_editable": False,
                    "for_organization": False,
                    "name": "Playbook2",
                    "description": "test",
                    "disabled": False,
                    "starting": True,
                    "owner": None,
                },
            ],
        },
        200,
        "/api/playbook",
    )
