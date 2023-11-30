import plotly.graph_objects as go
import matplotlib.pyplot as plt


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