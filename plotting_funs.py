import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st
# NB: to create plot to be displayed, it seems that you must not use return fig

# Function to plot data using Plotly
@st.cache_data
def plot_weather_data_plotly(timestamps, temperatures, humidities):
    # Create a figure with subplots
    fig = go.Figure()

    # Plot temperature
    fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperature (°C)'))

    # Plot humidity
    fig.add_trace(go.Scatter(x=timestamps, y=humidities, mode='lines+markers', name='Humidity (%)', yaxis='y2'))

    # Update layout to have two y-axes
    fig.update_layout(
        xaxis=dict(title='Timestamp'),
        yaxis=dict(title='Temperature (°C)'),
        yaxis2=dict(title='Humidity (%)', overlaying='y', side='right'),
        title='Weather Data Visualization for the last 7 days',
        showlegend=True
    )

    return fig
