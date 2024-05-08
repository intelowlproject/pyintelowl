from pyintelowl.exceptions import IntelOwlClientException
from tests.mocked_requests import (
    mocked_analyzer_config,
    mocked_ask_analysis_no_job_id,
    mocked_ask_analysis_no_status,
    mocked_ask_analysis_success,
    mocked_connector_config,
    mocked_playbook_config,
    mocked_raise_exception,
    mocked_send_analysis_success,
    mocked_send_playbook_analysis_success,
)
from tests.utils import BaseTest, get_file_data, mock_connections, patch


class TestGeneral(BaseTest):
    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_ask_analysis_success)
    )
    def test_ask_analysis_availability_success(self, mocked_requests):
        md5 = self.hash
        analyzers = ["test_1", "test_2"]
        result = self.client.ask_analysis_availability(md5, analyzers)
        self.assertIn("status", result)
        self.assertIn("job_id", result)

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_ask_analysis_no_status)
    )
    def test_ask_analysis_availability_no_status(self, mocked_requests):
        md5 = self.hash
        analyzers = ["test_1", "test_2"]
        with self.assertRaises(IntelOwlClientException):
            self.client.ask_analysis_availability(
                md5,
                analyzers,
            )

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_ask_analysis_no_job_id)
    )
    def test_ask_analysis_availability_no_job_id(self, mocked_requests):
        md5 = self.hash
        analyzers = ["test_1", "test_2"]
        with self.assertRaises(IntelOwlClientException):
            self.client.ask_analysis_availability(
                md5,
                analyzers,
            )

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_raise_exception)
    )
    def test_ask_analysis_availability_failure(self, mocked_requests):
        md5 = self.hash
        analyzers = ["test_1", "test_2"]
        with self.assertRaises(IntelOwlClientException):
            self.client.ask_analysis_availability(
                md5=md5,
                analyzers=analyzers,
            )

    @mock_connections(patch("requests.Session.get", side_effect=mocked_analyzer_config))
    def test_get_analyzer_config_success(self, mocked_requests):
        ac = self.client.get_analyzer_configs()
        self.assertNotEqual({}, ac)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_analyzer_config_failure(self, mocked_requests):
        with self.assertRaises(IntelOwlClientException):
            self.client.get_analyzer_configs()

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_connector_config)
    )
    def test_get_connector_config_success(self, mocked_requests):
        cc = self.client.get_connector_configs()
        self.assertNotEqual({}, cc)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_playbook_config))
    def test_get_playbook_config_success(self, mocked_requests):
        cc = self.client.get_playbook_configs()
        self.assertNotEqual({}, cc)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_connector_config_failure(self, mocked_requests):
        with self.assertRaises(IntelOwlClientException):
            self.client.get_connector_configs()

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_send_analysis_success)
    )
    def test_send_observable_analysis_request(self, mocked_requests):
        observable_name = self.domain
        analyzers_requested = ["test_1", "test_2"]
        connectors_requested = ["test_1", "test_2"]
        runtime_config = {"test_key": "test_param"}
        result = self.client.send_observable_analysis_request(
            observable_name,
            analyzers_requested=analyzers_requested,
            connectors_requested=connectors_requested,
            runtime_configuration=runtime_config,
        )
        self.assertIn("status", result)
        self.assertIn("job_id", result)
        self.assertIn("analyzers_running", result)

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_raise_exception)
    )
    def test_send_observable_analysis_request_failure(self, mocked_requests):
        observable_name = self.domain
        analyzers_requested = ["test_1", "test_2"]
        connectors_requested = ["test_1", "test_2"]
        runtime_config = {"test_key": "test_param"}
        with self.assertRaises(IntelOwlClientException):
            self.client.send_observable_analysis_request(
                observable_name,
                analyzers_requested=analyzers_requested,
                connectors_requested=connectors_requested,
                runtime_configuration=runtime_config,
            )

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_raise_exception)
    )
    def test_send_observable_analysis_request_failure_classify(self, mocked_requests):
        observable_name = self.domain
        analyzers_requested = ["test_1", "test_2"]
        connectors_requested = ["test_1", "test_2"]
        runtime_config = {"test_key": "test_param"}
        observable_classification = "unavailable"
        with self.assertRaises(IntelOwlClientException):
            self.client.send_observable_analysis_request(
                observable_name,
                analyzers_requested=analyzers_requested,
                connectors_requested=connectors_requested,
                runtime_configuration=runtime_config,
                observable_classification=observable_classification,
            )

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_send_analysis_success)
    )
    def test_send_file_analysis_request(self, mocked_requests):
        analyzers_requested = ["test_1", "test_2"]
        connectors_requested = ["test_1", "test_2"]
        filename = self.filepath
        binary = get_file_data(self.filepath)
        runtime_config = {"test_key": "test_param"}
        result = self.client.send_file_analysis_request(
            filename,
            binary,
            analyzers_requested=analyzers_requested,
            connectors_requested=connectors_requested,
            runtime_configuration=runtime_config,
        )
        self.assertIn("status", result)
        self.assertIn("job_id", result)
        self.assertIn("analyzers_running", result)

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_raise_exception)
    )
    def test_send_file_analysis_request_failure(self, mocked_requests):
        analyzers_requested = ["test_1", "test_2"]
        connectors_requested = ["test_1", "test_2"]
        filename = self.filepath
        binary = get_file_data(self.filepath)
        runtime_config = {"test_key": "test_param"}
        with self.assertRaises(IntelOwlClientException):
            self.client.send_file_analysis_request(
                filename,
                binary,
                analyzers_requested=analyzers_requested,
                connectors_requested=connectors_requested,
                runtime_configuration=runtime_config,
            )

    @mock_connections(
        patch(
            "requests.Session.post", side_effect=mocked_send_playbook_analysis_success
        )
    )
    def test_send_observable_playbook_analysis_request(self, mocked_requests):
        observable_name = self.domain
        runtime_config = {"test_key": "test_param"}
        playbook_requested = "TEST_PLAYBOOK"
        result = self.client.send_observable_analysis_playbook_request(
            observable_name,
            playbook_requested=playbook_requested,
            runtime_configuration=runtime_config,
        )

        self.assertIn("status", result)
        self.assertIn("job_id", result)
        self.assertIn("analyzers_running", result)

    @mock_connections(
        patch(
            "requests.Session.post", side_effect=mocked_send_playbook_analysis_success
        )
    )
    def test_send_file_playbook_analysis_request(self, mocked_requests):
        playbook_requested = "TEST_PLAYBOOK"
        filename = self.filepath
        binary = get_file_data(self.filepath)
        runtime_config = {"test_key": "test_param"}
        result = self.client.send_file_analysis_playbook_request(
            filename,
            binary,
            playbook_requested=playbook_requested,
            runtime_configuration=runtime_config,
        )

        self.assertIn("status", result)
        self.assertIn("job_id", result)
        self.assertIn("analyzers_running", result)

    def test_get_md5_observable(self):
        type_ = "observable"
        test_string = "test"
        hashed_value = self.client.get_md5(test_string, type_)
        self.assertEqual(hashed_value, "098f6bcd4621d373cade4e832627b4f6")

    def test_get_md5_binary(self):
        type_ = "binary"
        test_string = get_file_data(self.filepath)
        hashed_value = self.client.get_md5(test_string, type_)
        self.assertEqual(hashed_value, self.file_hash)

    def test_get_md5_file_success(self):
        type_ = "file"
        test_string = self.filepath
        hashed_value = self.client.get_md5(test_string, type_)
        self.assertEqual(hashed_value, self.file_hash)

    def test_get_md5_file_failure(self):
        type_ = "file"
        test_string = "/path/to/non-existent/file"
        with self.assertRaises(IntelOwlClientException):
            self.client.get_md5(test_string, type_)

    def test__get_observable_classification_ip(self):
        test_value = self.ip
        result = self.client._get_observable_classification(test_value)
        self.assertEqual(result, "ip")

    def test__get_observable_classification_domain(self):
        test_value = self.domain
        result = self.client._get_observable_classification(test_value)
        self.assertEqual(result, "domain")

    def test__get_observable_classification_url(self):
        test_value = self.url
        result = self.client._get_observable_classification(test_value)
        self.assertEqual(result, "url")

    def test__get_observable_classification_hash(self):
        test_value = self.hash
        result = self.client._get_observable_classification(test_value)
        self.assertEqual(result, "hash")

    def test__get_observable_classification_generic(self):
        test_value = self.generic
        result = self.client._get_observable_classification(test_value)
        self.assertEqual(result, "generic")
