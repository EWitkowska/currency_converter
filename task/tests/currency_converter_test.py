import sys
from pathlib import Path
import unittest

project_root = Path(__file__).resolve().parent.parent / ".."

sys.path.append(str(project_root))

from task.currency_converter import PriceCurrencyConverterToPLN


class TestPriceCurrencyConverterToPLN(unittest.TestCase):
    def setUp(self):
        self.currency_rates_data = {
            "USD": [{"rate": 1.2, "date": "2023-09-23"}],
            "EUR": [{"rate": 0.9, "date": "2023-09-23"}],
        }

    def test_convert_to_pln_valid_data(self):
        converter = PriceCurrencyConverterToPLN(self.currency_rates_data)

        converted_price = converter.convert_to_pln(
            currency="USD", price=100.0, precision=2
        )

        self.assertEqual(converted_price.price_in_source_currency, 100.0)
        self.assertEqual(converted_price.currency, "USD")
        self.assertEqual(converted_price.currency_rate, 1.2)
        self.assertEqual(converted_price.currency_rate_fetch_date, "2023-09-23")
        self.assertEqual(converted_price.price_in_pln, 120.0)

    def test_convert_to_pln_invalid_currency(self):
        converter = PriceCurrencyConverterToPLN(self.currency_rates_data)

        with self.assertRaises(ValueError):
            converter.convert_to_pln(currency="EBE", price=100.0)

    def test_convert_to_pln_precision(self):
        converter = PriceCurrencyConverterToPLN(self.currency_rates_data)

        converted_price = converter.convert_to_pln(
            currency="USD", price=100.0, precision=4
        )

        self.assertEqual(converted_price.price_in_pln, 120.0000)


if __name__ == "__main__":
    unittest.main()
