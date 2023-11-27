from datetime import datetime, date
import pandas as pd
from xbbg import blp
import requests
import csv
import streamlit as st
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

# Function to visualize data from CSV
def visualize_data(path_to_price_data):
    # Read the CSV file
    df = pd.read_csv(path_to_price_data)

    # Set the page title
    st.title('CSV Data Visualization')
    # Display the DataFrame
    st.write(df)

    # Assuming the date column is at index 0
    date_column_index = 0
    df[df.columns[date_column_index]] = pd.to_datetime(df[df.columns[date_column_index]], errors='coerce')

    # Set the index to the datetime column
    df.set_index(df.columns[0], inplace=True)


    # Extract headers
    headers = df.columns.tolist()

    # Allow the user to select which equity plot to display
    selected_ticker = st.selectbox('Select Ticker', headers, index=0)
    column_no = df.columns.get_loc((selected_ticker))


    # Automatically populate equities and currency fields based on the selected ticker symbol
    selected_equities = df.iloc[0, column_no]
    selected_currency = df.iloc[1, column_no]

    st.text_input("Equities", value=selected_equities, key='equities', disabled=True)
    st.text_input("Currency", value=selected_currency, key='currency', disabled=True)

    # Allow the user to select the time frame
    time_frame = st.selectbox('Select Time Frame', ['Last 5 Days', '1 Month', '6 Months', '1 Year', '5 Years'])

    # Resample the data based on the selected time frame
    if time_frame == 'Last 5 Days':
        df_resampled = df[selected_ticker][2:].astype("float64").last('5D')
    elif time_frame == '1 Month':
        df_resampled = df[selected_ticker][2:].astype("float64").last('1M')
    elif time_frame == '6 Months':
        df_resampled = df[selected_ticker][2:].astype("float64").last('6M')
    elif time_frame == '1 Year':
        df_resampled = df[selected_ticker][2:].astype("float64").last('1Y')
    elif time_frame == '5 Years':
        df_resampled = df[selected_ticker][2:].astype("float64").last('5Y')


    # Line plot for the selected equity and time frame
    st.subheader(f'Line plot for {selected_ticker} ({time_frame})')
    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", background_fill_color="black",
               border_fill_color="black", border_fill_alpha=0)
    p.line(df_resampled.index, df_resampled.values, line_width=2, color='green')
    p.circle(df_resampled.index, df_resampled.values, size=8, color='green')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = selected_ticker
    p.axis.axis_label_text_color = "white"
    p.axis.major_label_text_color = "white"
    p.axis.axis_label_text_font_style = "normal"
    p.axis.axis_label_text_font_size = "14pt"
    p.axis.axis_label_text_font = "Arial"
    p.axis.major_label_text_font_style = "normal"
    p.axis.major_label_text_font_size = "12pt"
    p.axis.major_label_text_font = "Arial"
    p.ygrid.grid_line_color = "lightgrey"
    p.ygrid.grid_line_alpha = 0.25
    p.xgrid.visible = False
    hover = HoverTool()
    hover.tooltips = [("Date", "@x{%F}"), (selected_ticker, "@y")]
    hover.formatters = {"@x": "datetime"}
    p.add_tools(hover)
    st.bokeh_chart(p)

    # Create a ColumnDataSource with the data for the bar graph
    source_bar = ColumnDataSource(data=dict(
        x=df_resampled.index,
        top=df_resampled.values.tolist()
    ))

    # Bar plot for the selected equity and time frame
    st.subheader(f'Bar plot for {selected_ticker} ({time_frame})')
    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", background_fill_color="black",
               border_fill_color="black", border_fill_alpha=0)
    p.vbar(x='x', top='top', width=0.5, color='green', line_width=10, source=source_bar)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = selected_ticker
    p.axis.axis_label_text_color = "white"
    p.axis.major_label_text_color = "white"
    p.axis.axis_label_text_font_style = "normal"
    p.axis.axis_label_text_font_size = "14pt"
    p.axis.axis_label_text_font = "Arial"
    p.axis.major_label_text_font_style = "normal"
    p.axis.major_label_text_font_size = "12pt"
    p.axis.major_label_text_font = "Arial"
    p.ygrid.grid_line_color = "lightgrey"
    p.ygrid.grid_line_alpha = 0.25
    p.xgrid.visible = False
    hover_bar = HoverTool()
    hover_bar.tooltips = [("Date", "@x{%F}"), (selected_ticker, "@top")]
    hover_bar.formatters = {"@x": "datetime"}
    p.add_tools(hover_bar)
    st.bokeh_chart(p)



def check_if_empty(ticker_symbols, start_date, frequency):
    # Determine today's date
    end_date = datetime.today()
    # Fetch price data from Bloomberg
    price_data = blp.bdh(
        tickers=ticker_symbols, flds=['last_price'], start_date=start_date, end_date=end_date, Per=frequency
    )
    if price_data.empty:
        return False

# Function to fetch price data from Bloomberg
def fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency, path_to_csv):
    # Fetch price data from Bloomberg
    price_data = blp.bdh(
        tickers=ticker_symbols, flds=['last_price'], start_date=start_date, end_date=end_date, Per=frequency
    )
    # Delete empty rows
    price_data.dropna(inplace=True, thresh=3, axis=0)

    price_data.columns = price_data.columns.droplevel(-1)
    header = [ticker_symbols, equities, currency]
    price_data.columns = header

    # Add timestamp to the file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "\\" + frequency + '_bloomberg_price_' + timestamp + '.csv'
    file_path = path_to_csv + file_name
    price_data.to_csv(file_path)


# Function to check if ticker exists on Bloomberg
def check_if_ticker_exists(ticker_symbols):
    today = date.today().replace(day=1)
    end_date = datetime.today()
    try:
        data = blp.bdh(
            tickers=ticker_symbols, flds=['last_price'], start_date=today, end_date=end_date, Per='D')
        return not data.empty
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# Function to log successful runs
def log_successful_run(log_file_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, "Success"])


# Function to run with default parameters
def run_with_defaults(path_to_tickers, log_file_path, path_to_csv):
    frequency = 'M'
    start_date = date.today().replace(day=1)
    run_fetch_data(path_to_tickers, frequency, start_date, path_to_csv)
    log_successful_run(log_file_path)

# Function to fetch data
def run_fetch_data(path_to_tickers, frequency, start_date, path_to_csv):
    bloomberg_equities = pd.read_csv(path_to_tickers, index_col=False)
    bloomberg_equities = bloomberg_equities.sort_values(by=['BBG Ticker'], ignore_index=True)

    ticker_symbols = bloomberg_equities['BBG Ticker']

    equities = bloomberg_equities['Equities']
    currency = bloomberg_equities['Currency']

    # Determine today's date
    end_date = datetime.today()

    empty_data = fetch_price_from_bloomberg(ticker_symbols, equities, currency, start_date, end_date, frequency, path_to_csv)
    return empty_data

# Function to add or delete data from CSV
def add_or_delete_data(path_to_tickers, path_to_csv):
    # Check for errors in user inputs
    errors = []
    st.title('Bloomberg Data Fetcher')

    # Read CSV file containing ticker symbols, equities, and currency
    bloomberg_equities = pd.read_csv(path_to_tickers)

    # Fetching list of currencies
    response = requests.get('https://open.er-api.com/v6/latest/USD')
    currency_data = response.json()
    currencies = list(currency_data['rates'].keys())

    # Add user input fields
    add_del = st.selectbox("Select Add or Delete ticker symbol", ['Add', 'Delete'], index=0)
    if add_del in ['Delete']:
        ticker_symbols = st.multiselect("Select ticker symbols", list(bloomberg_equities['BBG Ticker']))
        # Auto-populate equities and currency fields based on the selected ticker symbol
        if ticker_symbols:
            for ticker_symbol in ticker_symbols:
                selected_row = bloomberg_equities[bloomberg_equities['BBG Ticker'] == ticker_symbol]
                selected_equities = selected_row['Equities'].values[0]
                selected_currencies = selected_row['Currency'].values[0]

                st.text_input(f"Enter equities for {ticker_symbol}", value=selected_equities, disabled=True)
                st.text_input(f"Enter currencies for {ticker_symbol}", value=selected_currencies, disabled=True)
        else:
            errors.append("Empty field")

    else:
        ticker_symbols = st.text_input("Enter ticker symbols (separated by comma if multiple):", key="ticker_input")
        if len(ticker_symbols) == 0:
            errors.append("Can't leave field empty")

        # Process user inputs
        ticker_symbols_input_list = [s.strip() for s in ticker_symbols.split(',') if s.strip()]

        if ticker_symbols_input_list:
            try:
                bloomberg_equities = pd.read_csv(path_to_tickers, index_col=False)
                existing_tickers = list(bloomberg_equities['BBG Ticker'])
            except FileNotFoundError:
                existing_tickers = []

            if any(ticker in existing_tickers for ticker in ticker_symbols_input_list):
                existing_input_ticker = []
                for ticker in ticker_symbols_input_list:
                    if ticker in existing_tickers:
                        existing_input_ticker.append(ticker)
                st.error(f"Ticker symbol already exists.\n   {', '.join(existing_input_ticker)}")
                errors.append("Ticker symbol already exists.")

            elif any(not check_if_ticker_exists(ticker) for ticker in ticker_symbols_input_list):
                non_existing_tickers = [ticker for ticker in ticker_symbols_input_list if
                                    not check_if_ticker_exists(ticker)]
                st.error(f"The following ticker symbols do not exist on Bloomberg: {', '.join(non_existing_tickers)}")
                errors.append(f"The following ticker symbols do not exist on Bloomberg: {', '.join(non_existing_tickers)}")

            else:
                equities = st.text_input("Enter equities (separated by comma if multiple):")
                equities_input_list = [s.strip() for s in equities.split(',') if s.strip()]

                currency_input_list = []
                for ticker_symbol in ticker_symbols_input_list:
                    st.write(f"Select currency for {ticker_symbol}")
                    currency = st.selectbox(f"Select currency for {ticker_symbol}", currencies)
                    currency_input_list.append(currency)

                if len(ticker_symbols_input_list) != len(equities_input_list) or len(ticker_symbols_input_list) != len(
                        currency_input_list):
                    max_length = max(len(ticker_symbols_input_list), len(equities_input_list), len(currency_input_list))
                    if len(ticker_symbols_input_list) != max_length:
                        errors.append("Please provide all the required ticker symbols.")
                        st.error("Please provide all the required ticker symbols.")
                    if len(equities_input_list) != max_length:
                        errors.append("Please provide all the required equities.")
                        st.error("Please provide all the required equities.")
                    if len(currency_input_list) != max_length:
                        errors.append("Please provide all the required currencies.")
                        st.error("Please provide all the required currencies.")

                else:

                    frequency = st.selectbox("Select frequency", ['Daily', 'Weekly', 'Monthly'], index=2)
                    if frequency == 'Daily':
                        frequency = "D"
                    if frequency == 'Weekly':
                        frequency = "W"
                    if frequency == 'Monthly':
                        frequency = "M"

                    start_date_str = st.date_input("Select start date", value=date.today().replace(day=1),
                                                   min_value=date(1990, 1, 1),
                                                   max_value=date.today())
                    start_date = start_date_str.strftime('%Y-%m-%d')
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Add submit button
    if st.button("Submit", key="submit_button", disabled=bool(errors)):
        wait_label = st.empty()

        if add_del == 'Delete':
            if ticker_symbols:
                for ticker_symbol in ticker_symbols:
                    bloomberg_equities = bloomberg_equities[bloomberg_equities['BBG Ticker'] != ticker_symbol]
                bloomberg_equities.to_csv(path_to_tickers, index=False)
                st.write("Selected ticker symbols deleted successfully. Press Submit again if you want to delete more data")


        else:
            new_data = pd.DataFrame({
                'BBG Ticker': ticker_symbols_input_list,
                'Equities': equities_input_list,
                'Currency': currency_input_list
            })

            empty_data_error = check_if_empty(ticker_symbols, start_date, frequency)

            if empty_data_error == False:
                wait_label.text("Error......")
                errors.append("Empty data fetched, please check all the fields")
                st.error("\n".join(errors))
                print("Empty data fetched")

            if not errors:
                # Append the new data to the CSV file
                new_data.to_csv(path_to_tickers, mode='a', header=False, index=False)
                st.success("New Ticker added to CSV file")
                wait_label.text("Please wait while we fetch the requested data...")
                run_fetch_data(path_to_tickers, frequency, start_date, path_to_csv)
                st.write("Your file is ready to use")


if __name__ == '__main__':

    option = st.sidebar.radio(
        "Select an option",
        ('Visualize Data', 'Add/Delete Tickers')
    )

    today = date.today()
    # Read the CSV file
    #input for price data path
    path_to_price_data = input("Enter the path to the price data CSV file: ")
    #input for tickers path
    path_to_tickers = input("Enter the path to the tickers CSV file: ")
    #input for log file path
    log_file_path = input("Enter the path to the log file: ")
    #input for CSV path
    path_to_csv = input("Enter the path to the CSV folder: ")

    current_time = datetime.now().time()
    # automate the script to run at the first day of month and every monday
    if ((today.day == 1 or today.weekday() == 0) and datetime.strptime('20:30', '%H:%M').time() <= current_time <=
            datetime.strptime('20:35', '%H:%M').time()):
        run_with_defaults(path_to_tickers, log_file_path, path_to_csv)

    elif option == 'Visualize Data':
        visualize_data(path_to_price_data)
    elif option == 'Add/Delete Tickers':
        add_or_delete_data(path_to_tickers, path_to_csv)

    st.markdown(
        "<br><br><br><br><br><br><br><br><br><br><br><br><br><br><p style='text-align: center; color: white;'>Made with ❤️ by Shradha Maria</p>",
        unsafe_allow_html=True
    )
