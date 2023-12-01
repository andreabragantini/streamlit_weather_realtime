import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import seaborn as sns
sns.set()
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image       # this package is used to put images within streamlit
# Standard plotly imports
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.figure_factory as ff
from plotting_funs import plot_weather_data

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#%% Loading data

# define the API endpoint
API_URL = "https://weatherapi-com.p.rapidapi.com"
archive = "/current.json"

# headers
headers = {
	"X-RapidAPI-Key": "6a425b2a7bmshc1f059e65b98fb7p1cdd78jsn184965114ca2",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

# Function to geocode location to latitude and longitude
def geocode_location(location):

    #nominatim_service = Nominatim(user_agent="andrea.bragantini@upc.edu")
    #geolocator = RateLimiter(nominatim_service.geocode, min_delay_seconds=1)
    geolocator = Nominatim(user_agent="andrea.bragantini@upc.edu")
    location_info = geolocator.geocode(location)

    return location_info

    #if location_info:
    #    return location_info.latitude, location_info.longitude
    #else:
    #    return None

#%% Web app design

# title
st.title("Real-time Weather App")

# User input
location = st.text_input("Enter Location:", "Barcelona, Spain")
# geocode the location
coords = geocode_location(location)
#coords = str(lat) + "," + str(lon)
#coords = '53.1,-0.13'

#print(lat, lon)
st.write(coords)

# fun to make request
def get_weather_data(location):

    # get latitude and longitude
    lat, lon = geocode_location(location)
    coords = str(lat) + "," + str(lon)
    #coords = '53.1,-0.13'

    # create params dict
    querystring = {"q": coords}
    # make request
    response = requests.get(API_URL + archive, headers=headers, params=querystring)
    # store response
    data = response.json()

    return data

# if input is successful
if coords:

    st.write("Latitude:", coords[0], "Longitude:", coords[1])

    timestamps, temperatures, humidities = [], [], []

    # real-time operations
    while True:
        # get data with get request
        weather_data = get_weather_data(location)

        # Extract data from the API response
        timestamp = datetime.strptime(weather_data["location"]["localtime"], "%Y-%m-%d %H:%M")
        temperature = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]

        # Append data to lists
        timestamps.append(timestamp)
        temperatures.append(temperature)
        humidities.append(humidity)

        # crate the plot
        fig = plot_weather_data(timestamps, temperatures, humidities)

        # display the plot
        st.pyplot(fig)

        # Wait for a specified time before making the next request
        time.sleep(300)

else:
    st.write("Invalid location. Please enter a valid location.")


