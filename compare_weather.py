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

        temperature = humidity = precipitation = None
        if 'main' in weather_data:
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
        precipitation = weather_data.get('rain', {}).get('1h', 0) + weather_data.get('snow', {}).get('1h', 0)

        return {'temp': temperature, 'humidity': humidity, 'precipitation': precipitation}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenWeatherMap: {e}")
        return None

def get_differences(weather1, weather2):
    differences = {
        'temp_diff': abs(weather1['temp'] - weather2['temp']),
        'humidity_diff': abs(weather1['humidity'] - weather2['humidity']),
        'precipitation_diff': abs(weather1['precipitation'] - weather2['precipitation'])
    }
    return differences

if __name__ == '__main__':
    current_city = input('Enter current city: ').strip()
    current_weather = get_city_weather(current_city)

    destination_city = input('Enter destination city: ').strip()
    destination_weather = get_city_weather(destination_city)

    if current_weather and destination_weather:  # Ensure both weather data are valid
        differences = get_differences(current_weather, destination_weather)
        print(f"Differences between {current_city} and {destination_city}:")
        print(f"Temperature Difference: {differences['temp_diff']}°C")
        print(f"Humidity Difference: {differences['humidity_diff']}%")
        print(f"Precipitation Difference: {differences['precipitation_diff']}mm")
    else:
        print("Failed to retrieve weather data for one or both cities.")
