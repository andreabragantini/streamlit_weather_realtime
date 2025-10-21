"""
Script to test the OpenCage Geocoder API
Contains the function used in the main script to geolocate a location
"""
import os
import streamlit as st
from opencage.geocoder import OpenCageGeocode

# Define the custom exception for missing API key
class APIAuthError(Exception): ...

# NB: The OpenCage API key is now stored in .streamlit/secrets.toml, and must be retrieved
def get_api_key() -> str:
    # Prefer Streamlit secrets, fall back to env var
    key = st.secrets.get("OPENCAGE_API_KEY", None) or os.getenv("OPENCAGE_API_KEY")
    if not key:
        raise APIAuthError(
            "Missing OpenCage API key. Add OPENCAGE_API_KEY to .streamlit/secrets.toml "
            "or set the OPENCAGE_API_KEY environment variable."
        )
    return key

# There might be problems with the API key if not used for long time, therefore need proper error handling
def get_lat_long_opencage(city_name):

    try:
        opencage_api_key = get_api_key()
        OCG = OpenCageGeocode(opencage_api_key)
        data = OCG.geocode(city_name)

        if data and data[0]:
            location = data[0]['formatted']
            print(f"Found coordinates for {city_name}: {location}")
            latitude, longitude = data[0]['geometry']['lat'], data[0]['geometry']['lng']
            return latitude, longitude
        else:
            print(f"Could not find coordinates for {city_name}")
            return None

    except Exception as e:
        # Let the caller decide how to show this
        raise APIAuthError(f"An error occurred: {e}") from e


######################################################################################
#%% Test the API
if __name__ == "__main__":

    # Example usage:
    opencage_api_key = get_api_key()
    OCG = OpenCageGeocode(opencage_api_key)

    results = OCG.geocode(u'athens')
    print(u'%f;%f;%s;%s' % (results[0]['geometry']['lat'],
                            results[0]['geometry']['lng'],
                            results[0]['components']['country_code'],
                            results[0]['annotations']['timezone']['name']))
    # 37.983941;23.728305;gr;Europe/Athens

    # example with reverse geocoding
    results = OCG.reverse_geocode(14.666, 76.833)
    print(results[0]['formatted'])
    # Sirigedoddi, Gummagatta, India

    # example with language
    results = OCG.geocode(u'Athens, Texas', language='de')
    print(results[0]['components']['country'])
    # Vereinigte Staaten von Amerika

    ######################################################################################
    # test the function
    city_name = "New York"
    latitude, longitude = get_lat_long_opencage(city_name)

    print(f"Coordinates for {city_name}: Latitude {latitude}, Longitude {longitude}")

#%% Using geopy package and Nominatim service

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

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

