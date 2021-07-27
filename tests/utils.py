import json
import pathlib
from unittest import TestCase
from unittest.mock import patch  # noqa: F401

from pyintelowl.pyintelowl import IntelOwl
from tests import (
    MOCK_CONNECTIONS,
    TEST_JOB_ID,
    TEST_IP,
    TEST_DOMAIN,
    TEST_URL,
    TEST_HASH,
    TEST_GENERIC,
    TEST_FILE,
    TEST_FILE_HASH,
)

ROOT_DIR = pathlib.Path(__file__).parent.parent


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
        self.job_id = TEST_JOB_ID
        self.ip = TEST_IP
        self.url = TEST_URL
        self.domain = TEST_DOMAIN
        self.hash = TEST_HASH
        self.generic = TEST_GENERIC
        self.filepath = f"{ROOT_DIR}/test_files/{TEST_FILE}"
        self.file_hash = TEST_FILE_HASH


def mock_connections(decorator):
    return decorator if MOCK_CONNECTIONS else lambda x: x


def get_test_file_data(filepath):
    with open(filepath, "rb") as f:
        file = f.read()

    return file
