# Bloomberg Data Visualization and Management

## Overview

This repository contains Python scripts for visualizing Bloomberg price data and managing ticker symbols in a CSV file. Two versions of the data fetcher are available, each with a different user interface:

- `data_fetcher_streamlit.py`: Uses Streamlit for the user interface.
- `data_fetcher_tkinter.py`: Uses Tkinter for the user interface. This version offers a simplified interface focused on the addition of new ticker symbols without deletion or visualization capabilities.

## data_fetcher_streamlit.py: 
The script utilizes the Streamlit framework for the user interface and Bokeh for data visualization. The primary functionalities include:

- **Visualizing Data**: The script allows users to visualize historical price data for selected equities over different time frames.

- **Adding/Deleting Tickers**: Users can add new ticker symbols with corresponding equities and currencies to the CSV file. Additionally, existing ticker symbols can be deleted from the CSV file.

- **Automated Data Fetching**: The script can be set to run automatically at the first day of the month and every Monday, fetching data from Bloomberg and updating the CSV file.

## Requirements

- Python 3.x
- Pandas
- Xbbg
- Requests
- Streamlit
- Bokeh

Install the required packages using:

```bash
pip install pandas xbbg requests streamlit bokeh
```

## Usage
1. **Clone the Repository:**

    ```bash
    git clone https://github.com/SmartHacks25/FieldProject.git
    ```

2. **Run the Script:**

   For data_fetcher_streamlit.py

    ```bash
    streamlit run data_fetcher_streamlit.py
    ```

   For data_fetcher_tkinter.py
   
   ```bash
    python run data_fetcher_tkinter.py
    ```
   
   The script will prompt you to enter the paths to the required files:

    - Enter the path to the price data CSV file.
    - Enter the path to the tickers CSV file.
    - Enter the path to the log file.
    - Enter the path to the CSV folder.

    Follow the prompts to input these paths and press Enter to run the script.


3. **Automated Execution:**

    The script is set to run automatically at the first day of the month and every Monday between 20:30 and 20:35. Adjust the scheduling parameters in the script if needed.

## Customization

Feel free to customize the script according to your specific requirements. You can modify the data visualization settings, update the input prompts, or extend the functionality as needed.

