import sys
import logging
from unittest import TestCase, mock
from click.testing import CliRunner
from requests import Session
from pyintelowl.main import cli

from .mock_utils import MockResponse


logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestJobs(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_job_help(self):
        result = self.runner.invoke(cli, ["jobs", "-h"])
        assert "Manage Jobs" in result.output

    @mock.patch.object(Session, "get")
    def test_list_all_jobs(self, mock_get=None):
        mock_get.return_value = MockResponse(
            [],
            200,
            "/api/jobs",
        )
        result = self.runner.invoke(cli, ["jobs", "ls"])
        assert "List of Jobs" in result.output

    @mock.patch.object(Session, "get")
    def test_view_one_job(self, mock_get=None):
        mock_get.return_value = MockResponse(
            {
                "id": 1,
                "tags": [],
                "source": "root",
                "is_sample": True,
                "md5": "88e6168765e5bc7caf741743d00e825d",
                "observable_name": "wifiNetworkId=e7:9b:C3:AC:59:6B",
                "observable_classification": "generic",
                "file_name": "",
                "file_mimetype": "",
                "status": "failed",
                "analyzers_requested": ["WiGLE"],
                "run_all_available_analyzers": False,
                "analyzers_to_execute": ["WiGLE"],
                "analysis_reports": [
                    {
                        "name": "WiGLE",
                        "errors": ["too many values to unpack (expected 2)"],
                        "report": {},
                        "success": False,
                        "process_time": 0.000652313232421875,
                        "started_time": 1609169198.9222848,
                        "started_time_str": "2020-12-28 15:26:38",
                    }
                ],
                "received_request_time": "2020-12-28T15:26:38.746877Z",
                "finished_analysis_time": "2020-12-28T15:26:38.937221Z",
                "force_privacy": False,
                "disable_external_analyzers": False,
                "errors": [],
                "runtime_configuration": {},
            },
            200,
            "/api/job/1",
        )
        result = self.runner.invoke(cli, ["jobs", "view", "1"])
        assert "Job attributes" in result.output
        assert "Analysis Data" in result.output
        assert "Job ID: 1" in result.output
