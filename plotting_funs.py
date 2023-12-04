import plotly.graph_objects as go
import matplotlib.pyplot as plt

# NB: to create plot to be displayed, it seems that you must not use return fig

# Function to plot data
def plot_weather_data(timestamps, temperatures, humidities):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    ax1.plot(timestamps, temperatures, label="Temperature (°C)", marker='o')
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend()

    ax2.plot(timestamps, humidities, label="Humidity (%)", marker='o', color='orange')
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("Humidity (%)")
    ax2.legend()


# Function to plot data using Plotly
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
        title='Weather Data Visualization',
        showlegend=True
    )

