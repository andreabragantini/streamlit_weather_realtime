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
from plotting_funs import plot_weather_data_plotly
from geoloc_api import get_lat_long_opencage, APIAuthError
from weather_api_current import get_weather_data
from weather_api_hist import get_historical_weather_data

# Page setting
st.set_page_config(
    page_title="Real-Time Weather Data Dashboard",
    page_icon="✅",
    layout="wide",
)

# Disable warning on st.pyplot (the config option: deprecation.showPyplotGlobalUse)
st.set_option('deprecation.showPyplotGlobalUse', False)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#%% Web app design

# Title
st.title("Real-time Weather App")

# User input
location = st.text_input("Enter Location:", "Barcelona, Spain")

# Geocode the location
if location:
    with st.spinner("Geocoding…"):
        try:
            result = get_lat_long_opencage(location)

            if result is None:
                st.warning("Something went wrong in retrieving the location.")
                st.stop()

            lat, lon = result  # safe to unpack now
            coords = str(lat) + "," + str(lon)

        except APIAuthError as e:
            st.error(str(e))
            st.caption("Tip: The API key might be expired or updated. Check OPENCAGE_API_KEY to .streamlit/secrets.toml and restart the app.")
            st.stop()  # prevents the rest of the app from running


# Create a placeholder for the weather info
weather_placeholder = st.empty()

# if input is successful
if coords:

    # get data with get request
    weather_data = get_weather_data(location)

    # Extract data from the API response
    timestamp = datetime.strptime(weather_data["location"]["localtime"], "%Y-%m-%d %H:%M")
    temperature = weather_data["current"]["temp_c"]
    humidity = weather_data["current"]["humidity"]

    #####################################################################################
    ### Display weather data
    #####################################################################################

    with weather_placeholder.container():

        #st.header(f"Weather in {weather_data['location']['name']}, {weather_data['location']['country']}")

        # Set background color based on temperature
        background_color = '#FFD700' if weather_data['current']['temp_c'] > 10 else '#87CEEB'
        st.markdown(f'<style>body{{background-color: {background_color}; margin: 0; padding: 0;}}</style>',
                    unsafe_allow_html=True)

        localtime = weather_data['location']['localtime']
        localtime = datetime.strptime(localtime, "%Y-%m-%d %H:%M")

        condition = weather_data["current"]["condition"]["text"]
        condition_icon = weather_data['current']['condition']['icon']

        # container for time, condition and icon
        with st.container():

            time_col, condition_col, icon_col = st.columns([3, 1, 1])

            # Display time information on the left
            time_col.subheader(f'{localtime}')

            # Display condition info with icon on the right
            condition_col.metric("Condition:", f"{condition}")

            # Display condition info with icon on the right
            icon_col.image(f"https:{condition_icon}", width=100)


        #####################################################################################
        # 1st ROW - Principal Weather data
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Temperature (°C)", f"{weather_data['current']['temp_c']}°C")
        a2.metric("Feels Like (°C)", f"{weather_data['current']['feelslike_c']}°C")
        a3.metric("Humidity (%)", f"{weather_data['current']['humidity']}%")
        a4.metric("Wind (km/h)", f"{weather_data['current']['wind_kph']} km/h")

        # put a separator
        st.markdown("""---""")

        #####################################################################################
        # 2nd ROW - Additional Weather data
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            st.subheader("Additional Weather Data")
            st.write(f"Temperature: {weather_data['current']['temp_f']}°F")
            st.write(f"Pressure: {weather_data['current']['pressure_mb']} mb")
            st.write(f"Cloudiness: {weather_data['current']['cloud']}%")
            st.write(
                f"Visibility: {weather_data['current']['vis_km']} km ({weather_data['current']['vis_miles']} miles)")
            st.write(f"UV Index: {weather_data['current']['uv']}")

        with b2:
            st.subheader("Wind Data")
            st.write(f"Wind Speed: {weather_data['current']['wind_kph']} km/h")
            st.write(f"Wind Direction: {weather_data['current']['wind_dir']}")
            st.write(f"Gust Speed: {weather_data['current']['gust_kph']} km/h")
            st.write(f"Gust Speed: {weather_data['current']['gust_mph']} mph")


        with b3:
            st.subheader("Additional Information")
            st.write("Latitude:", lat, "Longitude:", lon)
            st.write("Country:", weather_data['location']['country'])
            st.write("Region:", weather_data['location']['region'])
            st.write("Timezone:", weather_data['location']['tz_id'])

        with b4:
            st.subheader("Last Updated")
            st.write(f"Local Time: {weather_data['location']['localtime']}")
            st.write(f"API Last Updated: {weather_data['current']['last_updated']}")

        # put a separator
        st.markdown("""---""")

        #####################################################################################
        ### Create an historic of weather data to be plotted
        #####################################################################################

        # Structures to store historic data to be plotted
        timestamps, temperatures, humidities = [], [], []

        # get historical weather of the previous 7 days
        historic_weather_data = get_historical_weather_data(coords)

        # Extract data from the API response
        for day in historic_weather_data['forecast']['forecastday']:
            for hour in day['hour']:
                timestamps.append(hour['time'])
                temperatures.append(hour['temp_c'])
                humidities.append(hour['humidity'])

        # other app design idea:
        # find a way to make different api calls every t time and store the data in a dataframe
        # to be later plotted real time in a chart'''

        #####################################################################################
        # 3rd ROW - Map and Historic Data
        c1, c2 = st.columns(2, gap='large')

        # Map
        map_data = pd.DataFrame({
            'lat': [weather_data['location']['lat']],
            'lon': [weather_data['location']['lon']],
        })

        with c1:
            st.map(map_data, zoom=10)

        # Historic Data Plot
        with c2:

            # crate the plot
            fig = plot_weather_data_plotly(timestamps, temperatures, humidities)

            # display the plot
            st.plotly_chart(fig)

        # put a separator
        st.markdown("""---""")

        #####################################################################################
        # Additional information
        with st.expander("More Information"):
            st.write("Historical weather data are available for the previous 7 days only with the free API plan")
            st.write("Real-time weather data are available every 15 mins with the free API plan")
            st.write("Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)")
            st.write("Geocoding data provided by [OpenCage](https://opencagedata.com/)")
            st.write("Map tiles by [OpenStreetMap](https://www.openstreetmap.org/)")
            st.write("Plot created with [Plotly](https://plotly.com/)")
            st.write("App created with [Streamlit](https://streamlit.io/)")
            st.write("Hosting service provided by [Streamlit](https://streamlit.io/)")
            st.write("Source code available on [GitHub](https://github.com/andreabragantini/streamlit_weather_realtime)")
            st.write("If you like this app, please consider giving it a ⭐ on GitHub.")
            st.write("Created by [Andrea Bragantini](https://www.linkedin.com/in/andrea-bragantini-693b50136/)")

        # Wait for a specified time before making the next request
        time.sleep(2)

else:
    st.write("Invalid location. Please enter a valid location.")


