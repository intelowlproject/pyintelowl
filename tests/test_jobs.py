from .utils import MockResponse, BaseTest
from pyintelowl.main import cli
from unittest import mock
from requests import Session


class TestJobs(BaseTest):
    def test_job_help(self):
        result = self.runner.invoke(cli, ["jobs", "-h"])
        assert "Manage Jobs" in result.output
        assert result.exception is None

    @mock.patch.object(
        Session,
        "get",
        return_value=MockResponse(
            [],
            200,
            "/api/jobs",
        ),
    )
    def test_list_all_jobs(self, mock_get=None):
        result = self.runner.invoke(cli, ["jobs", "ls"])
        assert "Requesting list of jobs.." in self.caplog.text
        assert "List of Jobs" in result.output
        assert result.exception is None

    @mock.patch.object(
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
    def test_view_one_job(self, mock_get=None):
        result = self.runner.invoke(cli, ["jobs", "view", "1"])
        print("CAPLOG", self.caplog.text)
        assert "Requesting Job" in self.caplog.text
        assert "Job attributes" in result.output
        assert "Analysis Data" in result.output
        assert "Job ID: 1" in result.output
        assert result.exception is None

    def test_poll(self):
        # TODO
        pass
