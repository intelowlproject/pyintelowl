import json
from unittest import TestCase
from unittest.mock import patch  # noqa: F401

from pyintelowl.pyintelowl import IntelOwl
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
        self.client = IntelOwl("test-token", "test-url")


def mock_connections(decorator):
    return decorator if MOCK_CONNECTIONS else lambda x: x


def mocked_requests(*args, **kwargs):
    return MockResponse({}, 200)
