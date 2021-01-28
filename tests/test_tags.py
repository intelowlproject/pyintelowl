from .utils import MockResponse, BaseTest
from pyintelowl.main import cli
from unittest import mock
from requests import Session


class TestTags(BaseTest):
    def test_tag_help(self):
        result = self.runner.invoke(cli, ["tags", "-h"])
        assert "Manage tags" in result.output
        assert result.exception is None

    @mock.patch.object(
        Session,
        "get",
        return_value=MockResponse(
            [],
            200,
            "/api/tags",
        ),
    )
    def test_list_all_tags(self, mock_get=None):
        result = self.runner.invoke(cli, ["tags", "ls"])
        assert "Requesting list of tags.." in self.caplog.text
        assert "List of tags" in result.output
        assert result.exception is None

    @mock.patch.object(
        Session,
        "get",
        return_value=MockResponse(
            {"id": 1, "label": "test-tag", "color": "green"},
            200,
            "/api/tag/1",
        ),
    )
    def test_view_one_tag(self, mock_get):
        result = self.runner.invoke(cli, ["tags", "view", "1"])
        assert "Requesting Tag" in self.caplog.text
        assert "List of tags" in result.output
        assert result.exception is None
