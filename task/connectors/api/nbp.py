import requests
from task.logger import CustomLogger


class NBPApiConnector:
    def __init__(self, enable_logging: bool = True):
        self.base_url = "http://api.nbp.pl/api/exchangerates/rates/A/"
        self.logger = CustomLogger(
            __name__, "nbp_api.log", enable_logging=enable_logging
        ).get_logger()

    def fetch_currency_rate(self, currency_code: str) -> dict:
        try:
            url = f"{self.base_url}{currency_code}/"
            headers = {"Accept": "application/json"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                rates_data = {
                    currency_code: [
                        {
                            "rate": data["rates"][0]["mid"],
                            "date": data["rates"][0]["effectiveDate"],
                        }
                    ]
                }
                return rates_data
            else:
                self.logger.error(
                    f"Failed to fetch currency rate for {currency_code}. Status code: {response.status_code}. Error: {response.text}"
                )
                return {}
        except Exception as err:
            self.logger.error(
                f"An error occurred while fetching currency rate for {currency_code} from NBP API: {err}"
            )
            return {}
