from pathlib import Path
from task.currency_utils import CurrencyDataFetcher
from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sqlite import SqliteDatabaseConnector
from .currency_converter import PriceCurrencyConverterToPLN
from .arguments import ArgumentParser
from .logger import CustomLogger

log_file = "currency_converter.log"
logger = CustomLogger(__name__, log_file, enable_logging=True).get_logger()

logger.info("Script started")


def main():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    base_dir = Path(__file__).resolve().parent.parent
    example_currency_rates_file_path = base_dir / "example_currency_rates.json"

    print(
        "This script allows you to convert prices from any currency to Polish Zloty (PLN)\n"
        "You can choose between two data sources: local or API (NBP)\n"
        "The converted amount will be saved to an appropriate database based on your selection\n"
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
            print(f"\nConversion price in PLN: {retrieved_data['price_in_pln']}\n")
            print(
                f"Latest rate: {retrieved_data['rate']} on {retrieved_data['date']}\n"
            )
        else:
            print("\nFailed to retrieve saved data\n")

    except ValueError as err:
        logger.error(f"ValueError: {err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        logger.exception("Traceback:")


if __name__ == "__main__":
    main()
    logger.info("Job done!")
