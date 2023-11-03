import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

import numpy as np

# Read the CSV file
df = pd.read_csv(r"/Users/shradhamaria/FieldPROJECT/xbbg/bloomberg_price.csv")

# Convert the index to datetime
df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])

# Set the index to the datetime column
df.set_index(df.columns[0], inplace=True)

# Set the page title
st.title('CSV Data Visualization')

# Display the DataFrame
st.write(df)

# Get the list of equities
equities = [col for col in df.columns if df[col].dtype == 'float64']

# Allow the user to select which equity plot to display
selected_equity = st.selectbox('Select Equity', equities)

# Allow the user to select the time frame
time_frame = st.selectbox('Select Time Frame', ['Last 5 Days', '1 Month', '6 Months', '1 Year', '5 Years'])

# Resample the data based on the selected time frame
if time_frame == 'Last 5 Days':
    df_resampled = df[selected_equity].last('5D')
elif time_frame == '1 Month':
    df_resampled = df[selected_equity].last('1M')
elif time_frame == '6 Months':
    df_resampled = df[selected_equity].last('6M')
elif time_frame == '1 Year':
    df_resampled = df[selected_equity].last('1Y')
elif time_frame == '5 Years':
    df_resampled = df[selected_equity].last('5Y')



# Line plot for the selected equity and time frame
st.subheader(f'Line plot for {selected_equity} ({time_frame})')
p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", background_fill_color="black", border_fill_color="black", border_fill_alpha=0)
p.line(df_resampled.index, df_resampled.values, line_width=2, color='green')
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = selected_equity
p.axis.axis_label_text_color = "white"
p.axis.major_label_text_color = "white"
p.ygrid.grid_line_color = "lightgrey"  # Set the color of the horizontal grid lines
p.ygrid.grid_line_alpha = 0.25  # Set the transparency of the grid lines
p.xgrid.visible = False  # Disable the vertical grid lines
hover = HoverTool()
hover.tooltips = [("Date", "@x{%F}"), (selected_equity, "@y")]
hover.formatters = {"@x": "datetime"}
p.add_tools(hover)
st.bokeh_chart(p)


# Create a ColumnDataSource with the data for the bar graph
source_bar = ColumnDataSource(data=dict(
    x=df_resampled.index,
    top=df_resampled.values.tolist()
))

# Bar plot for the selected equity and time frame
st.subheader(f'Bar plot for {selected_equity} ({time_frame})')
p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", background_fill_color="black", border_fill_color="black", border_fill_alpha=0)
p.vbar(x='x', top='top', width=0.5, color='green', line_width=10, source=source_bar)
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = selected_equity
p.axis.axis_label_text_color = "white"
p.axis.major_label_text_color = "white"
p.ygrid.grid_line_color = "lightgrey"  # Set the color of the horizontal grid lines
p.ygrid.grid_line_alpha = 0.25  # Set the transparency of the grid lines
p.xgrid.visible = False  # Disable the vertical grid lines
hover_bar = HoverTool()
hover_bar.tooltips = [("Date", "@x{%F}"), (selected_equity, "@top")]
hover_bar.formatters = {"@x": "datetime"}
p.add_tools(hover_bar)
st.bokeh_chart(p)

# Line plot for the selected equity and time frame
st.subheader(f'Line plot for {selected_equity} ({time_frame})')
fig, ax = plt.subplots()
ax.plot(df_resampled.index, df_resampled.values, color='green')
ax.set_xlabel('Date')
ax.set_ylabel(selected_equity)
plt.xticks(rotation=45)
ax.set_ylabel(selected_equity)
ax.set_facecolor('black')
ax.figure.set_facecolor('black')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.yaxis.label.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
st.pyplot(fig)

# Bar plot for the selected equity and time frame
st.subheader(f'Bar plot for {selected_equity} ({time_frame})')
fig, ax = plt.subplots()
ax.bar(df_resampled.index, df_resampled.values, color='green', width=15)
ax.set_xlabel('Date')
ax.set_ylabel(selected_equity)
plt.xticks(rotation=45)
ax.set_facecolor('black')
ax.figure.set_facecolor('black')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.yaxis.label.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)
st.pyplot(fig)


#
