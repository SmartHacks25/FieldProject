from datetime import datetime, date
import pandas as pd
from xbbg import blp
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import sys

def fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency, wait_label):
    price_data = blp.bdh(
        tickers=ticker_symbols, flds=['last_price'], start_date=start_date, end_date=end_date, Per=frequency
    )
    # to delete the empty rows which are the end days of month but not the working days
    price_data.dropna(inplace=True, thresh=3, axis=0)
    price_data.columns = price_data.columns.droplevel(-1)
    header = [ticker_symbols, equities, currency]
    price_data.columns = header

    file_name = frequency + '_bloomberg_price.csv'
    # Save the data to a CSV file
    price_data.to_csv(file_name)
    wait_label.config(text="Your file is ready to use.")

def check_if_ticker_exists(ticker_symbols):
    today = date.today()
    try:
        data = blp.bdh(tickers=ticker_symbols, flds=['last_price'], start_date=today, end_date=today, Per='D')
        return not data.empty
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

"""
def on_timeout(window):
    window.quit()
    run_with_defaults()

def run_with_defaults():
    frequency = 'M'
    start_date = date.today().replace(day=1)
    run_fetch_data(frequency, start_date)


def run_fetch_data(frequency, start_date):
    # Read ticker symbols, equities, and currency from the CSV file
    bloomberg_equities = pd.read_csv('bloomberg_tickers.csv', index_col=False)
    bloomberg_equities = bloomberg_equities.sort_values(by=['BBG Ticker'], ignore_index=True)

    ticker_symbols = bloomberg_equities['BBG Ticker']
    equities = bloomberg_equities['Equities']
    currency = bloomberg_equities['Currency']

    # Determine today's date
    end_date = datetime.today()

    fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency, wait_label)
"""

def create_input_window():

    global wait_label

    def on_submit():

        ticker_symbols = ticker_symbols_input.get()
        equities = equities_input.get()
        currency = currency_input.get()
        frequency = frequency_input.get()
        start_date_str = start_date_input.get()

        ticker_symbols_input_list = [s.strip() for s in ticker_symbols.split(',') if s.strip()]
        equities_input_list = [s.strip() for s in equities.split(',') if s.strip()]
        currency_input_list = [s.strip() for s in currency.split(',') if s.strip()]

        # Check inputs after receiving all the user inputs
        errors = []

        if ticker_symbols_input_list or equities_input_list or currency_input_list:
            if len(ticker_symbols_input_list) != len(equities_input_list) or len(ticker_symbols_input_list) != len(
                    currency_input_list):
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
            messagebox.showerror("Error", "\n".join(errors))

        else:
            wait_label.config(text="Please wait while we fetch the requested data...")
            if ticker_symbols_input_list or equities_input_list or currency_input_list:
                # Create DataFrame from user input
                new_data = pd.DataFrame({
                    'BBG Ticker': ticker_symbols_input_list,
                    'Equities': equities_input_list,
                    'Currency': currency_input_list
                })

                # Append the new data to the CSV file
                new_data.to_csv('bloomberg_tickers.csv', mode='a', header=False, index=False)
                print("New Ticker added to CSV file")

        # Read ticker symbols, equities, and currency from the CSV file
        bloomberg_equities = pd.read_csv('bloomberg_tickers.csv', index_col=False)
        bloomberg_equities = bloomberg_equities.sort_values(by=['BBG Ticker'], ignore_index=True)

        ticker_symbols = bloomberg_equities['BBG Ticker']
        equities = bloomberg_equities['Equities']
        currency = bloomberg_equities['Currency']

        # Determine today's date
        end_date = datetime.today()

        fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency,wait_label)
        window.destroy()

    window = tk.Tk()
    window.title('Bloomberg Data Fetcher')

    frame = ttk.Frame(window, padding=20)
    frame.grid(row=0, column=0)

    ttk.Label(frame, text="Enter ticker symbols (separated by comma if multiple):").grid(row=0, column=0, pady=10)
    ticker_symbols_input = ttk.Entry(frame, width=30)
    ticker_symbols_input.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Enter equities (separated by comma if multiple):").grid(row=1, column=0, pady=10)
    equities_input = ttk.Entry(frame, width=30)
    equities_input.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Enter currency (separated by comma if multiple):").grid(row=2, column=0, pady=10)
    currency_input = ttk.Entry(frame, width=30)
    currency_input.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Enter the frequency (D for daily, W for weekly, M for monthly, leave blank for default (Monthly):").grid(row=3, column=0,
                                                                                                 pady=10)
    frequency_input = ttk.Entry(frame, width=30)
    frequency_input.grid(row=3, column=1, pady=5)

    ttk.Label(frame, text="Enter the start date (YYYY-MM-DD, leave blank for default (1st day of the current month)): ").grid(row=4, column=0, pady=10)
    start_date_input = ttk.Entry(frame, width=30)
    start_date_input.grid(row=4, column=1, pady=5)

    submit_button = ttk.Button(frame, text="Submit", command=on_submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=20)

    wait_label = ttk.Label(frame, text="")
    wait_label.grid(row=6, column=0, columnspan=2, pady=10)

    #window.after(120000, on_timeout, window)
    window.mainloop()


if __name__ == "__main__":
    create_input_window()
    sys.setrecursionlimit(30000)
