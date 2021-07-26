from pyintelowl.exceptions import IntelOwlClientException
from .utils import (
    BaseTest,
    mock_connections,
    patch,
)
from .mocked_requests import (
    mocked_get_all_jobs,
    mocked_get_job_by_id,
    mocked_delete_job_by_id,
    mocked_kill_job,
    mocked_raise_exception,
)


class TestJobs(BaseTest):
    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_all_jobs))
    def test_get_all_jobs_success(self, mock_requests):
        all_jobs = self.client.get_all_jobs()
        self.assertIsInstance(all_jobs, list)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_all_jobs_failure(self, mock_requests):
        self.assertRaises(IntelOwlClientException, self.client.get_all_jobs)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_job_by_id))
    def test_get_job_by_id_valid(self, mock_requests):
        job_id = 1
        job = self.client.get_job_by_id(job_id)
        self.assertEqual(job.get("id", None), 1)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_job_by_id_invalid(self, mock_requests):
        job_id = 999
        self.assertRaises(IntelOwlClientException, self.client.get_job_by_id, job_id)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_delete_job_by_id)
    )
    def test_delete_job_by_id_success(self, mock_requests):
        job_id = 1
        deleted = self.client.delete_job_by_id(job_id)
        self.assertIsInstance(deleted, bool)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_raise_exception)
    )
    def test_delete_job_by_id_failure(self, mock_requests):
        job_id = 1
        self.assertRaises(IntelOwlClientException, self.client.delete_job_by_id, job_id)

    @mock_connections(patch("requests.Session.patch", side_effect=mocked_kill_job))
    def test_kill_running_job_success(self, mock_requests):
        job_id = 1
        killed = self.client.kill_running_job(job_id)
        self.assertIsInstance(killed, bool)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_raise_exception)
    )
    def test_kill_running_job_failure(self, mock_requests):
        job_id = 1
        self.assertRaises(IntelOwlClientException, self.client.kill_running_job, job_id)
