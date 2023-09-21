from pathlib import Path
import logging
from task.currency_utils import CurrencyDataFetcher
from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sqlite import SqliteDatabaseConnector
from task.currency_converter import PriceCurrencyConverterToPLN
from .arguments import ArgumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    base_dir = Path(__file__).resolve().parent.parent
    example_currency_rates_file_path = base_dir / "example_currency_rates.json"

    print(
        "This script allows you to convert prices from any currency to Polish Zloty (PLN)."
    )
    print("You can choose between two data sources: local or API (NBP).")
    print(
        "The converted amount will be saved to an appropriate database based on your selection.\n"
    )

    currency = str(input("Enter the currency code (e.g., EUR): "))
    amount = float(input("Enter the amount to convert: "))

    try:
        currency_data_fetcher = CurrencyDataFetcher(example_currency_rates_file_path)
        currency_rates_data = currency_data_fetcher.get_currency_rates_data(
            args.source, currency
        )
        converter = PriceCurrencyConverterToPLN(currency_rates_data)
        price_in_pln = converter.convert_to_pln(currency=currency, price=amount)

        if args.mode == "dev":
            db_connector = JsonFileDatabaseConnector()
        elif args.mode == "prod":
            db_connector = SqliteDatabaseConnector()
            db_connector.create_database()
        else:
            raise ValueError("Invalid mode argument")

        entity = {
            "currency": currency.lower(),
            "rate": price_in_pln.currency_rate,
            "price_in_pln": price_in_pln.price_in_pln,
            "date": price_in_pln.currency_rate_fetch_date,
        }

        new_id = db_connector.save(entity)
        retrieved_data = currency_data_fetcher.retrieve_data(new_id, db_connector)

        if retrieved_data:
            print("\nConversion data saved successfully to the database\n")
            print(f"ID: {retrieved_data['id']}")
            print(f"Currency: {retrieved_data['currency']}")
            print(f"Rate: {retrieved_data['rate']}")
            print(f"Price in PLN: {retrieved_data['price_in_pln']}")
            print(f"Date: {retrieved_data['date']}")
        else:
            print("\nFailed to retrieve saved data\n")

    except ValueError as err:
        print(f"\nError: {err}")
    except Exception as err:
        print(f"\nAn unexpected error occurred: {err}")


if __name__ == "__main__":
    main()
