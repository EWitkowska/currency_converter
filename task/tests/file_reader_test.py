import sys
from pathlib import Path
import unittest
import json
from unittest.mock import mock_open, patch

project_root = Path(__file__).resolve().parent.parent / ".."

sys.path.append(str(project_root))

from task.connectors.local.file_reader import LocalFileReader


class TestLocalFileReader(unittest.TestCase):
    def setUp(self):
        self.filename = "test.json"

    def test_read_existing_json_file(self):
        json_data = {
            "EUR": [
                {"date": "2023-09-01", "rate": 4.15},
                {"date": "2023-08-30", "rate": 4.1},
            ],
            "CZK": [
                {"date": "2023-09-01", "rate": 0.19},
                {"date": "2023-08-30", "rate": 0.18},
            ],
        }

        json_content = json.dumps(json_data, indent=4)

        m = mock_open(read_data=json_content)

        with patch("builtins.open", m):
            api_connector = LocalFileReader(self.filename, enable_logging=False)
            result = api_connector.read()

            print(result)

        self.assertEqual(result, json_data)

    def test_read_non_existent_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            api_connector = LocalFileReader(
                "non_existent_file.json", enable_logging=False
            )
            result = api_connector.read()

        self.assertEqual(result, {})

    def test_read_invalid_json_file(self):
        invalid_json_data = "invalid JSON"
        m = mock_open(read_data=invalid_json_data)

        with patch("builtins.open", m):
            api_connector = LocalFileReader(
                "invalid_json_file.json", enable_logging=False
            )
            result = api_connector.read()

        self.assertEqual(result, {})

    def test_read_empty_json_file(self):
        empty_json_data = "{}"
        m = mock_open(read_data=empty_json_data)

        with patch("builtins.open", m):
            api_connector = LocalFileReader(
                "empty_json_file.json", enable_logging=False
            )
            result = api_connector.read()

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
