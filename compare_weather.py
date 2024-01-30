#!/usr/bin/env python3

#!/usr/bin/env python3

import requests
import os  # Used for accessing environment variables

api_key = os.getenv('OPENWEATHERMAP_API_KEY')
if not api_key:
    raise ValueError("No API key provided. Set the OPENWEATHERMAP_API_KEY environment variable.")

def get_city_weather(city_name):

    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # or 'imperial' for Fahrenheit
    }

    try:
        r = requests.get(base_url, params=params)
        r.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        weather_data = r.json()
        if 'main' in weather_data:
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']

            if 'rain' in weather_data:
                precipitation = weather_data['rain']['1h']  # if there's rain info, keep it
            else:
                precipitation = 0   # no rain info? say that it's 0

        return {'temp':temperature,
                'humidity':humidity,
                'precipitation':precipitation}

    except requests.exceptions.RequestException as e:
        # Handle different types of errors (e.g., network error, timeout, etc.)
        print(f"Error fetching data from OpenWeatherMap: {e}")

if __name__ == '__main__':

    current_city = input('Enter current city: ').strip()
    current_weather = get_city_weather(current_city)

    destination_city = input('Enter destination city: ').strip()
    destination_weather = get_city_weather(destination_city)
