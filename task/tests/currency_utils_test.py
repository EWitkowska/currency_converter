import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

project_root = Path(__file__).resolve().parent.parent / ".."

sys.path.append(str(project_root))

from task.currency_utils import CurrencyDataFetcher


class TestCurrencyDataFetcher(unittest.TestCase):
    def setUp(self):
        self.example_currency_rates_file_path = "example_currency_rates.json"

        mock_api_connector = MagicMock()
        mock_api_connector.fetch_currency_rate.return_value = {
            "EUR": [{"date": "2023-09-22", "rate": 4.6069}]
        }

        self.currency_data_fetcher = CurrencyDataFetcher(
            self.example_currency_rates_file_path, enable_logging=False
        )

        self.currency_data_fetcher.api_connector = mock_api_connector

    @patch("task.currency_utils.LocalFileReader")
    def test_get_currency_rates_data_local_source(self, mock_file_reader):
        mock_file_reader_instance = mock_file_reader.return_value
        mock_file_reader_instance.read.return_value = {
            "EUR": [
                {"date": "2023-09-20", "rate": 4.6058},
            ]
        }

        currency_rates_data = self.currency_data_fetcher.get_currency_rates_data(
            source="local", currency="EUR"
        )

        self.assertEqual(currency_rates_data["EUR"][0]["rate"], 4.6058)
        self.assertEqual(currency_rates_data["EUR"][0]["date"], "2023-09-20")

    @patch("task.currency_utils.NBPApiConnector")
    def test_get_currency_rates_data_api_source(self, mock_api_connector):
        mock_api_connector_instance = mock_api_connector.return_value
        mock_api_connector_instance.fetch_currency_rate.return_value = {
            "EUR": [{"date": "2023-09-22", "rate": 4.6069}]
        }

        currency_rates_data = self.currency_data_fetcher.get_currency_rates_data(
            source="api", currency="EUR"
        )

        self.assertEqual(currency_rates_data["EUR"][0]["rate"], 4.6069)
        self.assertEqual(currency_rates_data["EUR"][0]["date"], "2023-09-22")


if __name__ == "__main__":
    unittest.main()
