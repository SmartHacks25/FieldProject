from datetime import datetime
import pandas as pd
import csv
import os
from xbbg import blp

if __name__ == "__main__":
    bloomberg_equities = pd.read_csv('tickers_equities.csv', index_col=False)
    bloomberg_equities.to_csv('bloomberg_tickers.csv', index=False)