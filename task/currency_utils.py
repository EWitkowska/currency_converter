from task.connectors.local.file_reader import LocalFileReader
from task.connectors.api.nbp import NBPApiConnector
from task.connectors.database.sqlite import CurrencyConversion


class CurrencyDataFetcher:
    def __init__(
        self, example_currency_rates_file_path: str, enable_logging: bool = True
    ):
        self.example_currency_rates_file_path = example_currency_rates_file_path
        self.api_connector = NBPApiConnector(enable_logging=enable_logging)

    def get_currency_rates_data(self, source: str, currency: str) -> dict:
        if source == "local":
            file_reader = LocalFileReader(self.example_currency_rates_file_path)
            return file_reader.read()
        elif source == "api":
            return self.api_connector.fetch_currency_rate(currency)
        else:
            raise ValueError("Invalid source argument")

    def retrieve_data(self, new_id: int, db_connector) -> dict:
        if new_id:
            data = db_connector.get_by_id(new_id)
            if data:
                if isinstance(data, CurrencyConversion):
                    data_dict = {
                        "id": data.id,
                        "currency": data.currency,
                        "rate": data.rate,
                        "price_in_pln": data.price_in_pln,
                        "date": data.date.strftime("%Y-%m-%d"),
                    }
                    return data_dict
                else:
                    return data
        return {}
