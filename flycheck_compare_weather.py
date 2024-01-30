#!/usr/bin/env python3

import requests
import argparse
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
        r.raise_for_status()
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
    return {
        'temp_diff': abs(weather1['temp'] - weather2['temp']),
        'humidity_diff': abs(weather1['humidity'] - weather2['humidity']),
        'precipitation_diff': abs(weather1['precipitation'] - weather2['precipitation'])
    }


def print_differences(current_weather, destination_weather, differences):
    print("\nWeather Comparison:\n")
    print(f"Current City Temperature: {current_weather['temp']}°C, Destination City Temperature: {destination_weather['temp']}°C")
    print(f"Temperature Difference: {differences['temp_diff']}°C")
    print(f"Current City Humidity: {current_weather['humidity']}%, Destination City Humidity: {destination_weather['humidity']}%")
    print(f"Humidity Difference: {differences['humidity_diff']}%")
    print(f"Current City Precipitation: {current_weather['precipitation']}mm, Destination City Precipitation: {destination_weather['precipitation']}mm")
    print(f"Precipitation Difference: {differences['precipitation_diff']}mm")

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Compare Weather between Two Cities')

    # Add the arguments
    parser.add_argument('-c', '--current_city', required=True, help='The current city')
    parser.add_argument('-d', '--destination_city', required=True, help='The destination city')

    # Parse the arguments
    args = parser.parse_args()

    # Retrieve the cities from the parsed arguments
    current_city = args.current_city
    destination_city = args.destination_city

    # Proceed with your existing logic using the provided city names
    current_weather = get_city_weather(current_city)
    destination_weather = get_city_weather(destination_city)

    if current_weather and destination_weather:
        differences = get_differences(current_weather, destination_weather)
        print_differences(current_weather, destination_weather, differences)
    else:
        print("Failed to retrieve weather data for one or both cities.")
