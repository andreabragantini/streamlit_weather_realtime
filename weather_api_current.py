"""
Script to test the Weather API
Contains the function used in the main script to stream CURRENT weather data
"""
import requests
import streamlit as st

# define the API endpoint
API_URL = "https://weatherapi-com.p.rapidapi.com"
archive = "/current.json"

# headers
headers = {
	"X-RapidAPI-Key": "6a425b2a7bmshc1f059e65b98fb7p1cdd78jsn184965114ca2",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

# fun to make request
@st.cache_data
def get_weather_data(coords):

    # create params dict
    querystring = {"q": coords}
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
    data = get_weather_data(coords)
    print(data)


