import duckdb

con = duckdb.connect("weather.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE clean_weather AS
    WITH ranked AS (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY weather_date
                   ORDER BY loaded_at DESC
               ) AS rn
        FROM raw_weather
    )
    SELECT weather_date, temp_max_f, precip_in, gust_max_mph, loaded_at
    FROM ranked
    WHERE rn = 1
      AND weather_date < current_date
    ORDER BY weather_date
""")

print("Raw rows:  ", con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()[0])
print("Clean rows:", con.execute("SELECT COUNT(*) FROM clean_weather").fetchone()[0])
print(con.execute("SELECT * FROM clean_weather").fetchdf())
con.close()