from .utils import BaseTest
from pyintelowl.main import cli
from .utils import mock_connections
from .mocked_requests import mock_tag_request


class TestTags(BaseTest):
    def test_tag_help(self):
        result = self.runner.invoke(cli, ["tags", "-h"])
        self.assertIs(result.exception, None)
        self.assertIn("Manage tags", result.output)

    @mock_connections(mock_tag_request("VIEW_ALL_TAGS"))
    def test_list_all_tags(self, mock_get=None):
        result = self.runner.invoke(cli, ["tags", "ls"])
        self.assertIs(result.exception, None)
        self.assertIn("Requesting list of tags..", self.caplog.text)
        self.assertIn("List of tags", result.output)

    @mock_connections(mock_tag_request("VIEW_ONE_TAG"))
    def test_view_one_tag(self, mock_get=None):
        result = self.runner.invoke(cli, ["tags", "view", "1"])
        self.assertIs(result.exception, None)
        self.assertIn("Requesting Tag", self.caplog.text)
        self.assertIn("List of tags", result.output)
