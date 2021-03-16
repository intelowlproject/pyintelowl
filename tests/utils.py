import json
import pytest
from unittest import TestCase
from click.testing import CliRunner
from tests import MOCK_CONNECTIONS


# class for mocking responses
class MockResponse:
    def __init__(self, json_data, status_code, uri):
        self.json_data = json_data
        self.status_code = status_code
        self.text = json.dumps(json_data)
        self.content = self.text.encode("utf-8")
        self.url = "http://localhost:80" + uri

    def json(self):
        return self.json_data

    @staticmethod
    def raise_for_status():
        pass


class BaseTest(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        caplog.set_level("INFO")
        self.caplog = caplog


def mock_connections(decorator):
    return decorator if MOCK_CONNECTIONS else lambda x: x
