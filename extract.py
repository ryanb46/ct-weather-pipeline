import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 41.77, "longitude": -72.44,   # Bolton, CT
    "daily": "temperature_2m_max,precipitation_sum,wind_gusts_10m_max",
    "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
    "precipitation_unit": "inch", "timezone": "America/New_York",
    "past_days": 7,
}

response = requests.get(url, params=params)
response.raise_for_status()   # crash loudly if the API fails
daily = response.json()["daily"]

for i in range(len(daily["time"])):
    print(daily["time"][i], daily["temperature_2m_max"][i],
          daily["precipitation_sum"][i], daily["wind_gusts_10m_max"][i])