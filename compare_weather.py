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

from rich.console import Console
from rich.table import Table

def get_temp_diff_color(difference):
    if difference > 5:
        return "bright_red"
    elif difference > 0:
        return "red"
    elif difference < -5:
        return "bright_blue"
    elif difference < 0:
        return "blue"
    else:
        return "white"

def print_differences(current_weather, destination_weather, differences, console=None):
    if console is None:
        console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Description", style="dim", width=20)
    table.add_column("Current City")
    table.add_column("Destination City")
    table.add_column("Difference", justify="right")

    # In the print_differences function, use this to determine the color
    temp_diff_color = get_temp_diff_color(differences['temp_diff'])

    # Add rows for temperature, humidity, and precipitation
    temp_diff_color = "red" if differences['temp_diff'] > 0 else "blue"
    table.add_row(
        "Temperature (°C)",
        f"{current_weather['temp']}",
        f"{destination_weather['temp']}",
        f"[{temp_diff_color}]{differences['temp_diff']}°C[/]"
    )

    table.add_row(
        "Humidity (%)",
        f"{current_weather['humidity']}",
        f"{destination_weather['humidity']}",
        f"{differences['humidity_diff']}%"
    )

    table.add_row(
        "Precipitation (mm)",
        f"{current_weather['precipitation']}",
        f"{destination_weather['precipitation']}",
        f"{differences['precipitation_diff']}mm"
    )

    console.print(table)

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
