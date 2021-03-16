from unittest import mock
from requests import Session
from .utils import MockResponse


def mock_job_request(job_request_type):
    if job_request_type == "VIEW_ONE_JOB":
        return mock.patch.object(
            Session,
            "get",
            return_value=MockResponse(
                {
                    "id": 1,
                    "tags": [],
                    "source": "test-user",
                    "md5": "test-md5-hash",
                    "observable_name": "test-observable_name",
                    "observable_classification": "test",
                    "status": "reported_without_fails",
                    "analysis_reports": [
                        {
                            "name": "test-analyzer",
                            "errors": [],
                            "report": {},
                            "success": True,
                        }
                    ],
                },
                200,
                "/api/job/1",
            ),
        )
    elif job_request_type == "VIEW_ALL_JOBS":
        return mock.patch.object(
            Session,
            "get",
            return_value=MockResponse(
                [],
                200,
                "/api/jobs",
            ),
        )
    else:
        raise Exception("Unknown job_request_type")


def mock_tag_request(tag_request_type):
    if tag_request_type == "VIEW_ONE_TAG":
        return mock.patch.object(
            Session,
            "get",
            return_value=MockResponse(
                {"id": 1, "label": "test-tag", "color": "green"},
                200,
                "/api/tag/1",
            ),
        )
    elif tag_request_type == "VIEW_ALL_TAGS":
        return mock.patch.object(
            Session,
            "get",
            return_value=MockResponse(
                [],
                200,
                "/api/tags",
            ),
        )
    else:
        raise Exception("Unknown tag_request_type")
