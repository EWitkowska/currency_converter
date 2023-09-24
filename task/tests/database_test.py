import sys
from datetime import datetime
from pathlib import Path
import unittest
from unittest.mock import MagicMock

project_root = Path(__file__).resolve().parent.parent / ".."

sys.path.append(str(project_root))

from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sqlite import SqliteDatabaseConnector


class TestJsonFileDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.db_connector = MagicMock(
            spec=JsonFileDatabaseConnector, enable_logging=False
        )
        self.test_id = 1

    def test_save_and_get_all(self):
        entity = {
            "currency": "usd",
            "rate": 1.2,
            "price_in_pln": 120.0,
            "date": "2023-09-23",
        }

        self.db_connector.save.return_value = 1

        saved_id = self.db_connector.save(entity)

        self.db_connector.save.assert_called_once_with(entity)

        self.assertNotEqual(saved_id, -1)
        self.assertEqual(saved_id, 1)

        fake_data_list = [MagicMock(currency="usd")]
        self.db_connector.get_all.return_value = fake_data_list

        all_data = self.db_connector.get_all()
        self.assertTrue(any(item.currency == "usd" for item in all_data))

    def test_get_by_id(self):
        entity = {
            "currency": "eur",
            "rate": 0.9,
            "price_in_pln": 90.0,
            "date": "2023-09-22",
        }

        self.db_connector.save.return_value = 2

        saved_id = self.db_connector.save(entity)

        fake_data = MagicMock(
            currency="eur",
            rate=0.9,
            price_in_pln=90.0,
            date="2023-09-22",
        )
        self.db_connector.get_by_id.return_value = fake_data

        retrieved_data = self.db_connector.get_by_id(saved_id)

        self.assertEqual(retrieved_data.currency, "eur")
        self.assertEqual(retrieved_data.rate, 0.9)
        self.assertEqual(retrieved_data.price_in_pln, 90.0)
        self.assertEqual(retrieved_data.date, "2023-09-22")


class TestSqliteDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.db_connector = MagicMock(SqliteDatabaseConnector, enable_logging=False)

    def test_save_and_get_all(self):
        entity = {
            "currency": "usd",
            "rate": 1.2,
            "price_in_pln": 120.0,
            "date": "2023-09-23",
        }

        self.db_connector.save.return_value = 1

        saved_id = self.db_connector.save(entity)

        self.db_connector.save.assert_called_once_with(entity)

        self.assertNotEqual(saved_id, -1)
        self.assertEqual(saved_id, 1)

        fake_data_list = [MagicMock(currency="usd")]
        self.db_connector.get_all.return_value = fake_data_list

        all_data = self.db_connector.get_all()
        self.assertTrue(any(item.currency == "usd" for item in all_data))

    def test_get_by_id(self):
        entity = {
            "currency": "eur",
            "rate": 0.9,
            "price_in_pln": 90.0,
            "date": "2023-09-22",
        }

        self.db_connector.save.return_value = 2

        saved_id = self.db_connector.save(entity)

        expected_date = datetime.strptime("2023-09-22", "%Y-%m-%d").date()

        fake_data = MagicMock(
            currency="eur",
            rate=0.9,
            price_in_pln=90.0,
            date=expected_date,
        )
        self.db_connector.get_by_id.return_value = fake_data

        retrieved_data = self.db_connector.get_by_id(saved_id)

        self.assertEqual(retrieved_data.currency, "eur")
        self.assertEqual(retrieved_data.rate, 0.9)
        self.assertEqual(retrieved_data.price_in_pln, 90.0)
        self.assertEqual(retrieved_data.date, expected_date)


if __name__ == "__main__":
    unittest.main()
