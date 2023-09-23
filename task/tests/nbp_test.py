import sys
from pathlib import Path
import unittest
from unittest.mock import patch, Mock
from requests import Response

project_root = Path(__file__).resolve().parent.parent / ".."

sys.path.append(str(project_root))

from task.connectors.api.nbp import NBPApiConnector


class TestNBPApiConnector(unittest.TestCase):
    def setUp(self):
        self.api_connector = NBPApiConnector(enable_logging=False)

    @patch("requests.get")
    def test_fetch_currency_rate_success(self, mock_requests_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": [{"mid": 4.5678, "effectiveDate": "2023-09-22"}]
        }
        mock_requests_get.return_value = mock_response

        currency_code = "USD"
        data = self.api_connector.fetch_currency_rate(currency_code)

        self.assertEqual(data, {"USD": [{"rate": 4.5678, "date": "2023-09-22"}]})

    @patch("requests.get")
    def test_fetch_currency_rate_failure(self, mock_requests_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_requests_get.return_value = mock_response

        currency_code = "AAA"
        data = self.api_connector.fetch_currency_rate(currency_code)

        self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()
