import pytest
import requests_mock
from compare_weather import get_city_weather, get_differences, print_differences

@pytest.fixture
def api_key():
    return "75e28cf00906095c31dc005c0ca6c38f"

@pytest.fixture
def mock_response():
    return {
        "main": {
            "temp": 20,
            "humidity": 50,
        },
        "rain": {
            "1h": 2
        }
    }

def test_get_city_weather(mock_response):
    city_name = "Test City"
    with requests_mock.Mocker() as m:
        m.get("http://api.openweathermap.org/data/2.5/weather", json=mock_response)
        result = get_city_weather(city_name)
        assert result == {'temp': 20, 'humidity': 50, 'precipitation': 2}

def test_get_differences():
    weather1 = {'temp': 20, 'humidity': 50, 'precipitation': 2}
    weather2 = {'temp': 25, 'humidity': 55, 'precipitation': 0}
    expected_diffs = {'temp_diff': 5, 'humidity_diff': 5, 'precipitation_diff': 2}
    assert get_differences(weather1, weather2) == expected_diffs

def test_print_differences(capsys):  # capsys is a built-in pytest fixture that captures sys output
    weather1 = {'temp': 20, 'humidity': 50, 'precipitation': 2}
    weather2 = {'temp': 25, 'humidity': 55, 'precipitation': 0}
    differences = {'temp_diff': 5, 'humidity_diff': 5, 'precipitation_diff': 2}
    print_differences(weather1, weather2, differences)
    captured = capsys.readouterr()  # Capture the print output
    assert "Temperature Difference: 5°C" in captured.out
    assert "Humidity Difference: 5%" in captured.out
    assert "Precipitation Difference: 2mm" in captured.out
