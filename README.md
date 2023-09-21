# Currency Converter

This Python script allows users to convert prices from any currency to Polish Zloty (PLN) using two different sources for currency exchange rates: a local JSON file and the NBP API (National Bank of Poland).

## Features

1. **User Input**: Users can input the following information:
   - Currency code (e.g., EUR)
   - Amount to convert
   - Source of currency exchange rates (local JSON or NBP API)

2. **Exchange Rate Fetching**: The script fetches the latest currency exchange rates from the selected source:
   - Local JSON file: `example_currency_rates.json`
   - NBP API: Utilizes the API provided by the National Bank of Poland

3. **Conversion**: It calculates and displays the converted amount in PLN based on the input currency and amount, using the fetched exchange rates.

4. **Database Storage**: The converted amount is saved to an appropriate database, depending on the script's mode:
   - Development (dev) mode uses a JSON file (`database.json`) as the database.
   - Production (prod) mode uses an SQLite database (`db.sqlite3`) and creates the database if it doesn't exist.

## Usage

To run the script, execute it with the desired mode and input parameters:

```shell
python currency_converter.py --source <source> --mode <mode>

**Examples:**

```shell
# Example 1: Using local JSON data in development mode
python currency_converter.py --source local --mode dev

# Example 2: Using NBP API data in production mode
python currency_converter.py --source api --mode prod

### Requirements

Before running the Currency Conversion script, please ensure the following requirements are met:

- **Python 3.8+**: Make sure you have Python version 3.8 or higher installed on your system.

To install the required Python packages, you can use `pip` and the provided `requirements.txt` file. Navigate to the project directory in your terminal and run the following command:

```bash
pip install -r requirements.txt
