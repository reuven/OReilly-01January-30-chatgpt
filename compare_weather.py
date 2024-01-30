#!/usr/bin/env python3

#!/usr/bin/env python3

import requests
import os  # Used for accessing environment variables

# Ensure you have set your API key as an environment variable
api_key = os.getenv('OPENWEATHERMAP_API_KEY')
if not api_key:
    raise ValueError("No API key provided. Set the OPENWEATHERMAP_API_KEY environment variable.")

base_url = 'http://api.openweathermap.org/data/2.5/weather'

params = {
    'q': 'Chicago',
    'appid': api_key,
    'units': 'metric'  # or 'imperial' for Fahrenheit
}

try:
    r = requests.get(base_url, params=params)
    r.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    # Process the data (assuming JSON response)
    weather_data = r.json()
    # Now you can extract and use specific pieces of data from weather_data as needed
    print(weather_data)


except requests.exceptions.RequestException as e:
    # Handle different types of errors (e.g., network error, timeout, etc.)
    print(f"Error fetching data from OpenWeatherMap: {e}")
