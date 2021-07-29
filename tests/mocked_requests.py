from .utils import (
    MockResponse,
    get_file_data,
    ROOT_DIR,
    TEST_FILE,
)


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
        "api/get_analyzer_configs",
    )


def mocked_ask_analysis_success(*args, **kwargs):
    return MockResponse(
        {
            "job_id": 1,
            "status": "running",
            "analyzers_to_execute": ["test_1", "test_2"],
        },
        200,
        "api/ask_analysis_availability",
    )


def mocked_ask_analysis_no_status(*args, **kwargs):
    return MockResponse(
        {
            "job_id": 1,
        },
        200,
        "api/ask_analysis_availability",
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
        "api/analyze_observable",
    )


def mocked_ask_analysis_no_job_id(*args, **kwargs):
    return MockResponse(
        {
            "status": "running",
        },
        200,
        "api/ask_analysis_availability",
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
        "/api/job/1",
    )


def mocked_get_all_jobs(*args, **kwargs):
    return MockResponse(
        [],
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
        200,
        "/api/jobs/1/kill",
    )


def mocked_download_job_sample(*args, **kwargs):
    return MockResponse(
        get_file_data(f"{ROOT_DIR}/test_files/{TEST_FILE}"),
        200,
        "/api/jobs/1/download_sample",
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
