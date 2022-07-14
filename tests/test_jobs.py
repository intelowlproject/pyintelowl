from pyintelowl.exceptions import IntelOwlClientException
from tests.mocked_requests import (
    mocked_analyzer_healthcheck,
    mocked_connector_healthcheck,
    mocked_delete_job_by_id,
    mocked_download_job_sample,
    mocked_get_all_jobs,
    mocked_get_job_by_id,
    mocked_kill_analyzer,
    mocked_kill_connector,
    mocked_kill_job,
    mocked_raise_exception,
    mocked_retry_analyzer,
    mocked_retry_connector,
)
from tests.utils import BaseTest, get_file_data, mock_connections, patch


class TestJobs(BaseTest):
    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_all_jobs))
    def test_get_all_jobs_success(self, mock_requests):
        all_jobs = self.client.get_all_jobs()
        self.assertIsInstance(all_jobs, dict)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_all_jobs_failure(self, mock_requests):
        self.assertRaises(IntelOwlClientException, self.client.get_all_jobs)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_job_by_id))
    def test_get_job_by_id_valid(self, mock_requests):
        job = self.client.get_job_by_id(self.job_id)
        self.assertEqual(job.get("id", None), 1)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_job_by_id_invalid(self, mock_requests):
        job_id = 999
        self.assertRaises(IntelOwlClientException, self.client.get_job_by_id, job_id)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_delete_job_by_id)
    )
    def test_delete_job_by_id_success(self, mock_requests):
        deleted = self.client.delete_job_by_id(self.job_id)
        self.assertIsInstance(deleted, bool)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_raise_exception)
    )
    def test_delete_job_by_id_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException, self.client.delete_job_by_id, self.job_id
        )

    @mock_connections(patch("requests.Session.patch", side_effect=mocked_kill_job))
    def test_kill_running_job_success(self, mock_requests):
        killed = self.client.kill_running_job(self.job_id)
        self.assertIsInstance(killed, bool)

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_raise_exception)
    )
    def test_kill_running_job_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException, self.client.kill_running_job, self.job_id
        )

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_download_job_sample)
    )
    def test_download_job_sample(self, mocked_requests):
        file_data = get_file_data(self.filepath)
        downloaded = self.client.download_sample(self.job_id)
        self.assertEqual(downloaded, file_data)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_download_job_sample_failure(self, mocked_requests):
        self.assertRaises(
            IntelOwlClientException, self.client.download_sample, self.job_id
        )

    @mock_connections(patch("requests.Session.patch", side_effect=mocked_kill_analyzer))
    def test_kill_analyzer_success(self, mock_requests):
        killed = self.client.kill_analyzer(self.job_id, self.analyzer_name)
        self.assertIsInstance(killed, bool)

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_raise_exception)
    )
    def test_kill_analyzer_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.kill_analyzer,
            self.job_id,
            self.analyzer_name,
        )

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_kill_connector)
    )
    def test_kill_connector_success(self, mock_requests):
        killed = self.client.kill_connector(self.job_id, self.connector_name)
        self.assertIsInstance(killed, bool)

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_raise_exception)
    )
    def test_kill_connector_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.kill_connector,
            self.job_id,
            self.connector_name,
        )

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_retry_analyzer)
    )
    def test_retry_analyzer_success(self, mock_requests):
        success = self.client.retry_analyzer(self.job_id, self.analyzer_name)
        self.assertIsInstance(success, bool)

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_raise_exception)
    )
    def test_retry_analyzer_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.retry_analyzer,
            self.job_id,
            self.analyzer_name,
        )

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_retry_connector)
    )
    def test_retry_connector_success(self, mock_requests):
        success = self.client.retry_connector(self.job_id, self.connector_name)
        self.assertIsInstance(success, bool)

    @mock_connections(
        patch("requests.Session.patch", side_effect=mocked_raise_exception)
    )
    def test_retry_connector_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.retry_connector,
            self.job_id,
            self.connector_name,
        )

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_analyzer_healthcheck)
    )
    def test_analyzer_healthcheck_success(self, mock_requests):
        status = self.client.analyzer_healthcheck(self.analyzer_name)
        self.assertIsInstance(status, bool)
        self.assertTrue(status)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_analyzer_healthcheck_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.analyzer_healthcheck,
            self.analyzer_name,
        )

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_connector_healthcheck)
    )
    def test_connector_healthcheck_success(self, mock_requests):
        status = self.client.connector_healthcheck(self.connector_name)
        self.assertIsInstance(status, bool)
        self.assertTrue(status)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_connector_healthcheck_failure(self, mock_requests):
        self.assertRaises(
            IntelOwlClientException,
            self.client.connector_healthcheck,
            self.connector_name,
        )
