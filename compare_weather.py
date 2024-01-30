#!/usr/bin/env python3

import requests

base_url = 'http://api.openweathermap.org/data/2.5/weather'

params = {'q':'Chicago',
          'appid':api_key,
          'units':metric}

r = requests.get(base_url, params=params)
