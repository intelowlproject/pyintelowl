from unittest.mock import patch

from tests.mocked_requests import mocked_get_all_playbooks, mocked_get_playbook_by_name
from tests.utils import BaseTest, mock_connections


class TestPlaybooks(BaseTest):
    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_playbook_by_name)
    )
    def test_get_playbook_by_name(self, mock_requests):
        playbook = self.client.get_playbook_by_name(self.playbook_name)
        self.assertEqual(playbook.get("name", ""), "Playbook1")
        self.assertEqual(playbook.get("type", []), ["test"])
        self.assertTrue(playbook.get("analyzers", []))
        self.assertEqual(playbook.get("analyzers", []), ["Analyzer1"])
        self.assertFalse(playbook.get("connectors", []))
        self.assertFalse(playbook.get("pivots", []))
        self.assertFalse(playbook.get("visualizers", []))
        self.assertEqual(playbook.get("description", ""), "test")

    @mock_connections(
        patch("requests.Session.get", side_effect=mocked_get_all_playbooks)
    )
    def test_get_all_playbooks(self, mock_requests):
        playbooks = self.client.get_all_playbooks()
        self.assertEqual(playbooks.get("count", 0), 2)
        self.assertEqual(playbooks.get("total_pages", 0), 1)
        self.assertTrue(playbooks.get("results", []))
        self.assertEqual(len(playbooks.get("results", [])), 2)

        results = playbooks.get("results", [])
        self.assertEqual(results[0].get("name", ""), "Playbook1")
        self.assertEqual(results[1].get("name", ""), "Playbook2")
