from .utils import BaseTest
from pyintelowl.main import cli
from .utils import mock_connections
from .mocked_requests import mock_job_request


class TestJobs(BaseTest):
    def test_job_help(self):
        result = self.runner.invoke(cli, ["jobs", "-h"])
        assert "Manage Jobs" in result.output
        assert result.exception is None

    @mock_connections(mock_job_request("VIEW_ALL_JOBS"))
    def test_list_all_jobs(self, mock_get=None):
        result = self.runner.invoke(cli, ["jobs", "ls"])
        self.assertIn("Requesting list of jobs..", self.caplog.text)
        self.assertIs(result.exception, None)
        self.assertIn("List of Jobs", result.output)

    @mock_connections(mock_job_request("VIEW_ONE_JOB"))
    def test_view_one_job(self, mock_get=None):
        result = self.runner.invoke(cli, ["jobs", "view", "1"])
        self.assertIn("Requesting Job", self.caplog.text)
        self.assertIs(result.exception, None, "Exception Caught!!!")
        self.assertIn("Job attributes", result.output)
        self.assertIn("Analysis Data", result.output)
        self.assertIn("Job ID: 1", result.output)

    def test_poll(self):
        # TODO
        pass
