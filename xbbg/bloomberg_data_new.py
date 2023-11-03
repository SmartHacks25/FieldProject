from datetime import datetime, date
import pandas as pd
from xbbg import blp


def fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency):
    price_data = blp.bdh(tickers=ticker_symbols, flds=['last_price'], start_date=start_date, end_date=end_date,
                         Per=frequency)
    # to delete the empty rows which are the end days of month but not the working days
    price_data.dropna(inplace=True, thresh=3, axis=0)
    price_data.columns = price_data.columns.droplevel(-1)
    header = [ticker_symbols, equities, currency]
    price_data.columns = header

    file_name = frequency + '_bloomberg_price.csv'
    # Save the data to a CSV file
    price_data.to_csv(file_name)
    print("done")

def check_if_ticker_exists(ticker_symbols):
    today = date.today()
    try:
        data = blp.bdh(tickers=ticker_symbols, flds=['last_price'], start_date=today, end_date=today, Per='D')
        return not data.empty
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


if __name__ == "__main__":


    while True:

        # Get input for ticker symbols, equities, and currency
        ticker_symbols_input = input("Enter ticker symbols (separated by comma if multiple): ")
        equities_input = input("Enter equities (separated by comma if multiple): ")
        currency_input = input(
            "Enter currency in the format Eg, USD, EUR (separated by comma if multiple): ")

        ticker_symbols_input_list = [s.strip() for s in ticker_symbols_input.split(',') if s.strip()]
        equities_input_list = [s.strip() for s in equities_input.split(',') if s.strip()]
        currency_input_list = [s.strip() for s in currency_input.split(',') if s.strip()]

        frequency = input("Enter the frequency (D for daily, W for weekly, M for monthly, leave blank for default (Monthly): ").strip()

        start_date_str = input("Enter the start date (YYYY-MM-DD, leave blank for default (1st day of the current month)): ")

        # Check inputs after receiving all the user inputs
        errors = []

        if ticker_symbols_input_list or equities_input_list or currency_input_list:
            if len(ticker_symbols_input_list) != len(equities_input_list) or len(ticker_symbols_input_list) != len(currency_input_list):
                errors.append("Please provide all the required inputs.")
            else:
                try:
                    bloomberg_equities = pd.read_csv('bloomberg_tickers.csv', index_col=False)
                    existing_tickers = list(bloomberg_equities['BBG Ticker'])
                except FileNotFoundError:
                    existing_tickers = []

                if all(ticker in existing_tickers for ticker in ticker_symbols_input_list):
                    errors.append("Ticker symbol already exists.")

                elif any(not check_if_ticker_exists(ticker) for ticker in ticker_symbols_input_list):
                    non_existing_tickers = [ticker for ticker in ticker_symbols_input_list if
                                            not check_if_ticker_exists(ticker)]
                    errors.append(
                        f"The following ticker symbols do not exist on Bloomberg: {', '.join(non_existing_tickers)}")

                else:
                    continue

        if frequency not in ['D', 'W', 'M'] and not frequency:
            frequency = 'M'
        elif frequency not in ['D', 'W', 'M']:
            errors.append("Invalid frequency. Please enter D for daily, W for weekly, or M for monthly.")

        if not start_date_str:
            start_date = date.today().replace(day=1)
        else:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            except ValueError:
                errors.append("Incorrect date format. Please provide the date in the format YYYY-MM-DD.")

        if errors:
            for error in errors:
                print(error)
        elif ticker_symbols_input_list or equities_input_list or currency_input_list:

            # Create DataFrame from user input
            new_data = pd.DataFrame({
                'BBG Ticker': ticker_symbols_input_list,
                'Equities': equities_input_list,
                'Currency': currency_input_list
            })

            # Append the new data to the CSV file
            new_data.to_csv('bloomberg_tickers.csv', mode='a', header=False, index=False)
            print("New Ticker added to CSV file")
            break
        else:
            break


    # Read ticker symbols, equities and currency from the CSV file
    bloomberg_equities = pd.read_csv('bloomberg_tickers.csv', index_col=False)
    bloomberg_equities = bloomberg_equities.sort_values(by=['BBG Ticker'], ignore_index=True)

    ticker_symbols = bloomberg_equities['BBG Ticker']
    equities = bloomberg_equities['Equities']
    currency = bloomberg_equities['Currency']

    # Determine today's date
    end_date = datetime.today()

    fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency)
