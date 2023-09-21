from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:
    def __init__(self, currency_rates_data):
        self.currency_rates_data = currency_rates_data

    def convert_to_pln(
        self, *, currency: str, price: float, precision: int = 2
    ) -> ConvertedPricePLN:
        if currency in self.currency_rates_data:
            latest_rate = self.currency_rates_data[currency][0]
            rate = latest_rate["rate"]
            rate_fetch_date = latest_rate["date"]
            price_in_pln = Decimal(price * rate).quantize(
                Decimal("0.{}".format("0" * precision)), rounding=ROUND_HALF_UP
            )

            return ConvertedPricePLN(
                price_in_source_currency=price,
                currency=currency,
                currency_rate=rate,
                currency_rate_fetch_date=rate_fetch_date,
                price_in_pln=float(price_in_pln),
            )
        else:
            raise ValueError(f"No currency rate data found for {currency}")
