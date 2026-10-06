import requests
import duckdb
from datetime import datetime

# 1. EXTRACT: ask the API for the data
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 41.77, "longitude": -72.44,   # Bolton, CT
    "daily": "temperature_2m_max,precipitation_sum,wind_gusts_10m_max",
    "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
    "precipitation_unit": "inch", "timezone": "America/New_York",
    "past_days": 7,
}
response = requests.get(url, params=params)
response.raise_for_status()
daily = response.json()["daily"]

# 2. LOAD: save it into a table in weather.duckdb
con = duckdb.connect("weather.duckdb")
con.execute("""
    CREATE TABLE IF NOT EXISTS raw_weather (
        weather_date  DATE,
        temp_max_f    DOUBLE,
        precip_in     DOUBLE,
        gust_max_mph  DOUBLE,
        loaded_at     TIMESTAMP
    )
""")

loaded_at = datetime.now()
rows = []
for i in range(len(daily["time"])):
    rows.append((daily["time"][i], daily["temperature_2m_max"][i],
                 daily["precipitation_sum"][i], daily["wind_gusts_10m_max"][i],
                 loaded_at))

con.execute("BEGIN")
con.executemany("INSERT INTO raw_weather VALUES (?, ?, ?, ?, ?)", rows)
con.execute("COMMIT")

print("Rows in table:", con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()[0])
con.close()