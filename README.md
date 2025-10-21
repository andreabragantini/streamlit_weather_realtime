# streamlit_weather_realtime
This repo contains code to create a simple web app interface to visualize real-time weather data.
Data is gathered from the WeatherAPI freely available in RapidAPI marketplace.

### How to read the repository

Edit `/streamlit_app.py` to customize this app

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

The `streamlit_app.py` file contains all the python code needed for the design of the web app.

Images and other media, like data are located in the same directory in the dedicated folders.

`requirements.txt` contains the list of the pyhton packages needed for the project. They have to be installed in the current environment.

`css` files are used for web development and contains information about the style (margins, colors, etc). Edit at your own risk.

The `.streamlit` directory contains a file storing **theme settings** for streamlit, which is quite easy to edit to change the aspect of the web app.  

This application is hosted on GitHub and deployed via Streamlit Community Cloud. You can access it here: [Weather Realtime App](https://weatherrealtime.streamlit.app/).
*Note: The app may enter a sleep state after periods of inactivity and could take a few moments to wake up when first accessed.*
