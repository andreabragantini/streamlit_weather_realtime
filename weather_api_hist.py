"""
Script to test the Weather API
Contains the function used in the main script to stream HISTORICAL weather data
NB: the API free tier allows to get historical data only for the PREVIOUS 7 days
"""
import requests
import streamlit as st
from datetime import datetime, timedelta

# define the API endpoint
API_URL = "https://weatherapi-com.p.rapidapi.com"
archive = "/history.json"

# headers
headers = {
	"X-RapidAPI-Key": "6a425b2a7bmshc1f059e65b98fb7p1cdd78jsn184965114ca2",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

# fun to make request
@st.cache_data
def get_historical_weather_data(coords):

    # get current time
    date = datetime.now().strftime("%Y-%m-%d")

    date_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # create params dict
    querystring = {"q": coords, "dt": date_from, "end_dt": date, "lang": "en"}
    # make request
    response = requests.get(API_URL + archive, headers=headers, params=querystring)
    # store response
    data = response.json()

    return data

# Example usage:
if __name__ == "__main__":

    ######################################################################################
    # test the API
    coords = '53.1,-0.13'
    data = get_historical_weather_data(coords)
    print(data)


