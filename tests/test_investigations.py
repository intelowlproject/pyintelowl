from unittest.mock import patch

from pyintelowl import IntelOwlClientException
from tests.mocked_requests import (
    mocked_get_investigation_by_id,
    mocked_get_investigation_tree_by_id,
)
from tests.utils import BaseTest, mock_connections


class TestInvestigations(BaseTest):
    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_investigation_by_id)
    )
    def test_get_investigation_by_id(self, mock_requests):
        investigation = self.client.get_investigation_by_id(self.job_id)
        self.assertEqual(investigation.get("id", None), 1)
        self.assertEqual(investigation.get("tags"), [])
        self.assertEqual(investigation.get("total_jobs", 2), 2)
        self.assertEqual(investigation.get("jobs", []), [1])
        self.assertEqual(investigation.get("status", ""), "concluded")
        self.assertTrue(investigation.get("for_organization", False))
        self.assertEqual(
            investigation.get("name", ""), "Analyzer1: https://www.test.com"
        )
        self.assertEqual(investigation.get("description", ""), "test_description")
        self.assertEqual(
            investigation.get("start_time", ""), "2024-11-13T07:42:17.534614Z"
        )
        self.assertEqual(
            investigation.get("end_time", ""), "2024-11-13T07:42:35.861687Z"
        )
        self.assertEqual(investigation.get("owner", ""), "admin")

        investigation = self.client.get_investigation_by_id(str(self.job_id))
        self.assertEqual(investigation.get("id", None), 1)
        self.assertEqual(investigation.get("tags"), [])
        self.assertEqual(investigation.get("total_jobs", 2), 2)
        self.assertEqual(investigation.get("jobs", []), [1])
        self.assertEqual(investigation.get("status", ""), "concluded")
        self.assertTrue(investigation.get("for_organization", False))
        self.assertEqual(
            investigation.get("name", ""), "Analyzer1: https://www.test.com"
        )
        self.assertEqual(investigation.get("description", ""), "test_description")
        self.assertEqual(
            investigation.get("start_time", ""), "2024-11-13T07:42:17.534614Z"
        )
        self.assertEqual(
            investigation.get("end_time", ""), "2024-11-13T07:42:35.861687Z"
        )
        self.assertEqual(investigation.get("owner", ""), "admin")

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_investigation_by_id)
    )
    def test_get_investigation_by_id_invalid(self, mock_requests):
        job_id = 999
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_by_id, job_id
        )

        job_id = "999"
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_by_id, job_id
        )

        job_id = ""
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_by_id, job_id
        )

        job_id = None
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_by_id, job_id
        )

        job_id = "a"
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_by_id, job_id
        )

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_investigation_tree_by_id)
    )
    def test_get_investigation_tree_by_id(self, mock_requests):
        investigation = self.client.get_investigation_tree_by_id(self.job_id)
        self.assertEqual(
            investigation.get("name", ""), "InvestigationName: https://www.test.com"
        )
        self.assertEqual(investigation.get("owner", ""), 1)
        self.assertNotEqual(investigation.get("jobs", []), [])

        jobs = investigation.get("jobs")[0]
        self.assertEqual(jobs.get("pk", None), 1)
        self.assertEqual(jobs.get("analyzed_object_name", ""), "https://www.test.com")
        self.assertEqual(jobs.get("playbook", ""), "Playbook1")
        self.assertEqual(jobs.get("status", ""), "reported_without_fails")
        self.assertEqual(
            jobs.get("received_request_time", ""),
            "2024-11-13T07:42:17.534614Z",
        )
        self.assertFalse(investigation.get("is_sample", True))

        children = jobs.get("children")[0]
        self.assertEqual(children.get("pk", 0), 2)
        self.assertEqual(children.get("analyzed_object_name", ""), "test.0")
        self.assertEqual(children.get("pivot_config", ""), "Pivot1")
        self.assertEqual(children.get("playbook", ""), "Playbook2")
        self.assertEqual(children.get("status", ""), "reported_without_fails")
        self.assertEqual(
            children.get("received_request_time", ""), "2024-11-13T07:42:35.243833Z"
        )
        self.assertTrue(children.get("is_sample", False))

        investigation = self.client.get_investigation_tree_by_id(str(self.job_id))
        self.assertEqual(
            investigation.get("name", ""), "InvestigationName: https://www.test.com"
        )
        self.assertEqual(investigation.get("owner", ""), 1)
        self.assertNotEqual(investigation.get("jobs", []), [])

        jobs = investigation.get("jobs")[0]
        self.assertEqual(jobs.get("pk", None), 1)
        self.assertEqual(jobs.get("analyzed_object_name", ""), "https://www.test.com")
        self.assertEqual(jobs.get("playbook", ""), "Playbook1")
        self.assertEqual(jobs.get("status", ""), "reported_without_fails")
        self.assertEqual(
            jobs.get("received_request_time", ""),
            "2024-11-13T07:42:17.534614Z",
        )
        self.assertFalse(investigation.get("is_sample", True))

        children = jobs.get("children")[0]
        self.assertEqual(children.get("pk", 0), 2)
        self.assertEqual(children.get("analyzed_object_name", ""), "test.0")
        self.assertEqual(children.get("pivot_config", ""), "Pivot1")
        self.assertEqual(children.get("playbook", ""), "Playbook2")
        self.assertEqual(children.get("status", ""), "reported_without_fails")
        self.assertEqual(
            children.get("received_request_time", ""), "2024-11-13T07:42:35.243833Z"
        )
        self.assertTrue(children.get("is_sample", False))

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_investigation_tree_by_id)
    )
    def test_get_investigation_tree_by_id_invalid(self, mock_requests):
        job_id = 999
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_tree_by_id, job_id
        )

        job_id = "999"
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_tree_by_id, job_id
        )

        job_id = ""
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_tree_by_id, job_id
        )

        job_id = None
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_tree_by_id, job_id
        )

        job_id = "a"
        self.assertRaises(
            IntelOwlClientException, self.client.get_investigation_tree_by_id, job_id
        )
