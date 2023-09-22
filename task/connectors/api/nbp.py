import requests
from task.logger import get_logger

logger = get_logger(__name__, "nbp_api.log")


class NBPApiConnector:
    def __init__(self):
        self.base_url = "http://api.nbp.pl/api/exchangerates/rates/A/"

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
                logger.error(
                    f"Failed to fetch currency rate for {currency_code}. Status code: {response.status_code}. Error: {response.text}"
                )
                return {}
        except Exception as err:
            logger.error(
                f"An error occurred while fetching currency rate for {currency_code} from NBP API: {err}"
            )
            return {}
