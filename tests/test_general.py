from pyintelowl.exceptions import IntelOwlClientException
from .utils import (
    BaseTest,
    mock_connections,
    patch,
)
from .mocked_requests import (
    mocked_analyzer_config,
    mocked_raise_exception,
)


class TestGeneral(BaseTest):
    @mock_connections(patch("requests.Session.get", side_effect=mocked_analyzer_config))
    def test_get_analyzer_config_success(self, mocked_requests):
        ac = self.client.get_analyzer_configs()
        self.assertNotEqual({}, ac)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_analyzer_config_failure(self, mocked_requests):
        self.assertRaises(IntelOwlClientException, self.client.get_analyzer_configs)
