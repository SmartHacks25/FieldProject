import blpapi
import pandas as pd
from datetime import datetime

def fetch_data_from_bloomberg(ticker_symbols, start_date, end_date):
    session_options = blpapi.SessionOptions()
    session = blpapi.Session(session_options)
    session.start()

    service_ref_data = session.getService("//blp/refdata")
    request = service_ref_data.createRequest("HistoricalDataRequest")
    for ticker in ticker_symbols:
        request.getElement("securities").appendValue(ticker)
    request.getElement("fields").appendValue("PX_LAST")
    request.getElement("fields").appendValue("CURRENCY")
    request.set("startDate", start_date.strftime('%Y%m%d'))
    request.set("endDate", end_date.strftime('%Y%m%d'))

    session.sendRequest(request)

    data = []
    while True:
        event = session.nextEvent()
        if event.eventType() == blpapi.Event.RESPONSE or event.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for msg in event:
                security_data = msg.getElement("securityData")
                ticker = security_data.getElement("security").getValue()
                field_data = security_data.getElement("fieldData")
                for i in range(field_data.numValues()):
                    row = [ticker]
                    for j in range(len(field_data.getValue(i).elements())):
                        row.append(field_data.getValue(i).getElement(j).getValue())
                    data.append(row)
        if event.eventType() == blpapi.Event.RESPONSE:
            break

    session.stop()

    data_df = pd.DataFrame(data, columns=["Ticker", "Date", "Price", "Currency"])
    data_df.set_index("Date", inplace=True)

    price_file = 'bloomberg_data.csv'
    data_df.to_csv(price_file)

    return data_df.head()

if __name__ == "__main__":
    # Read ticker symbols from the CSV file
    ticker_symbols_df = pd.read_csv('tickersymbols.csv')
    ticker_symbols = ticker_symbols_df['Ticker'].tolist()

    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    end_date = datetime.today()

    retrieved_data = fetch_data_from_bloomberg(ticker_symbols, start_date, end_date)
    print(f"Monthly data fetched from {start_date_str} to {end_date.strftime('%Y-%m-%d')} (first 5 rows):")
    print(retrieved_data)
