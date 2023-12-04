import streamlit as st
import time
import pandas as pd
import seaborn as sns
sns.set()
from datetime import datetime
from PIL import Image       # this package is used to put images within streamlit
# Standard plotly imports
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.figure_factory as ff
from plotting_funs import plot_weather_data, plot_weather_data_plotly
from geoloc_api import get_lat_long_opencage
from weather_api import get_weather_data

# Page setting
st.set_page_config(layout="wide")
# Disable warning on st.pyplot (the config option: deprecation.showPyplotGlobalUse)
st.set_option('deprecation.showPyplotGlobalUse', False)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#%% Web app design

# title
st.title("Real-time Weather App")

# User input
location = st.text_input("Enter Location:", "Barcelona, Spain")
# geocode the location
lat, lon = get_lat_long_opencage(location)
coords = str(lat) + "," + str(lon)

# if input is successful
if coords:

    st.write("Latitude:", lat, "Longitude:", lon)

    timestamps, temperatures, humidities = [], [], []

    # Create a placeholder for the plot
    plot_placeholder = st.empty()

    # real-time operations
    while True:
        # get data with get request
        weather_data = get_weather_data(location)

        # Extract data from the API response
        timestamp = datetime.strptime(weather_data["location"]["localtime"], "%Y-%m-%d %H:%M")
        temperature = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]

        # create an historic of weather data to be plotted
        # Append data to lists
        #timestamps.append(timestamp)
        #temperatures.append(temperature)
        #humidities.append(humidity)

        # crate the plot
        #fig = plot_weather_data(timestamps, temperatures, humidities)
        #fig = plot_weather_data_plotly(timestamps, temperatures, humidities)

        # display the plot
        #st.pyplot(fig)


        # Display weather data
        #st.header(f"Weather in {weather_data['location']['name']}, {weather_data['location']['country']}")
        st.subheader(f"As of {weather_data['location']['localtime']}")

        # Set background color based on temperature
        if weather_data['current']['temp_c'] > 25:
            st.markdown('<style>body{background-color: #FFD700;}</style>', unsafe_allow_html=True)  # Warm color
        else:
            st.markdown('<style>body{background-color: #87CEEB;}</style>', unsafe_allow_html=True)  # Cool color

        # Weather icons
        condition_icon = weather_data['current']['condition']['icon']
        st.image(f"https:{condition_icon}", width=100)

        # 1st ROW - Principal Weather data
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Temperature (°C)", f"{weather_data['current']['temp_c']}°C")
        a2.metric("Feels Like (°C)", f"{weather_data['current']['feelslike_c']}°C")
        a3.metric("Humidity (%)", f"{weather_data['current']['humidity']}%")
        a4.metric("Wind (km/h)", f"{weather_data['current']['wind_kph']} km/h")

        # 2nd ROW - Additional Weather data
        b1, b2, b3 = st.columns(3)
        with b1:
            st.subheader("Current Weather")
            st.write(f"Temperature: {weather_data['current']['temp_c']}°C ({weather_data['current']['temp_f']}°F)")
            st.write(f"Condition: {weather_data['current']['condition']['text']}")
            st.write(f"Humidity: {weather_data['current']['humidity']}%")
            st.write(f"Wind: {weather_data['current']['wind_kph']} km/h, {weather_data['current']['wind_dir']}")
            st.write(f"Pressure: {weather_data['current']['pressure_mb']} mb")
            st.write(f"Cloudiness: {weather_data['current']['cloud']}%")

        with b2:
            st.subheader("Additional Information")
            st.write(
                f"Feels Like: {weather_data['current']['feelslike_c']}°C ({weather_data['current']['feelslike_f']}°F)")
            st.write(
                f"Visibility: {weather_data['current']['vis_km']} km ({weather_data['current']['vis_miles']} miles)")
            st.write(f"UV Index: {weather_data['current']['uv']}")
            st.write(f"Gust Speed: {weather_data['current']['gust_kph']} km/h")

        with b3:
            st.subheader("Last Updated")
            st.write(f"Local Time: {weather_data['location']['localtime']}")
            st.write(f"API Last Updated: {weather_data['current']['last_updated']}")


        # Additional information
        with st.expander("More Information"):
            st.subheader("Current Weather")
            st.write(f"Condition: {weather_data['current']['condition']['text']}")
            st.write(f"Wind Direction: {weather_data['current']['wind_dir']}")
            st.write(f"Pressure: {weather_data['current']['pressure_mb']} mb")

        # Map
        map_data = pd.DataFrame({
            'lat': [weather_data['location']['lat']],
            'lon': [weather_data['location']['lon']],
        })
        st.map(map_data, zoom=10)

        # Wait for a specified time before making the next request
        time.sleep(61)

else:
    st.write("Invalid location. Please enter a valid location.")


