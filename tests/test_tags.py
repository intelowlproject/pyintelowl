from pyintelowl.exceptions import IntelOwlClientException
from tests.mocked_requests import (
    mocked_create_tag,
    mocked_delete_tag_by_id,
    mocked_edit_tag,
    mocked_get_all_tags,
    mocked_get_tag_by_id,
    mocked_raise_exception,
)
from tests.utils import BaseTest, mock_connections, patch


class TestTags(BaseTest):
    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_all_tags))
    def test_get_all_tags_success(self, mock_requests):
        all_tags = self.client.get_all_tags()
        self.assertIsInstance(all_tags, list)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_all_tags_failure(self, mock_requests):
        self.assertRaises(IntelOwlClientException, self.client.get_all_tags)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_get_tag_by_id))
    def test_get_tag_by_id_valid(self, mock_requests):
        tag_id = 1
        tag = self.client.get_tag_by_id(tag_id)
        self.assertEqual(tag.get("id", None), 1)
        self.assertIn("label", tag)
        self.assertIn("color", tag)

    @mock_connections(patch("requests.Session.get", side_effect=mocked_raise_exception))
    def test_get_tag_by_id_invalid(self, mock_requests):
        tag_id = 999
        self.assertRaises(IntelOwlClientException, self.client.get_tag_by_id, tag_id)

    @mock_connections(patch("requests.Session.post", side_effect=mocked_create_tag))
    def test_create_tag_success(self, mock_requests):
        label = "test-tag"
        color = "white"
        new_tag = self.client.create_tag(label, color)
        self.assertIn("id", new_tag)
        self.assertEqual(new_tag.get("label", None), "test-tag")
        self.assertEqual(new_tag.get("color", None), "white")

    @mock_connections(
        patch("requests.Session.post", side_effect=mocked_raise_exception)
    )
    def test_create_tag_failure(self, mock_requests):
        label = "test-tag"
        color = "white"
        self.assertRaises(IntelOwlClientException, self.client.create_tag, label, color)

    @mock_connections(patch("requests.Session.put", side_effect=mocked_edit_tag))
    def test_edit_tag_valid_id(self, mock_requests):
        tag_id = 1
        label = "modified-test-tag"
        color = "black"
        modified_tag = self.client.edit_tag(tag_id, label, color)
        self.assertEqual(modified_tag.get("id", None), 1)
        self.assertEqual(modified_tag.get("label", None), "modified-test-tag")
        self.assertEqual(modified_tag.get("color", None), "black")

    @mock_connections(patch("requests.Session.put", side_effect=mocked_raise_exception))
    def test_edit_tag_invalid_id(self, mock_requests):
        tag_id = 999
        label = "modified-test-tag"
        color = "black"
        self.assertRaises(
            IntelOwlClientException, self.client.edit_tag, tag_id, label, color
        )

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_delete_tag_by_id)
    )
    def test_delete_tag_by_id_success(self, mock_requests):
        tag_id = 1
        deleted = self.client.delete_tag_by_id(tag_id)
        self.assertIsInstance(deleted, bool)

    @mock_connections(
        patch("requests.Session.delete", side_effect=mocked_raise_exception)
    )
    def test_delete_tag_by_id_failure(self, mock_requests):
        tag_id = 1
        self.assertRaises(IntelOwlClientException, self.client.delete_tag_by_id, tag_id)
