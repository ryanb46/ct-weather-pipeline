import sys
import duckdb

con = duckdb.connect("weather.duckdb")

# Each check counts BAD rows. 0 = pass.
checks = {
    "table is not empty":
        "SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END FROM clean_weather",
    "no missing values":
        """SELECT COUNT(*) FROM clean_weather
           WHERE weather_date IS NULL OR temp_max_f IS NULL
              OR precip_in IS NULL OR gust_max_mph IS NULL""",
    "no duplicate dates":
        "SELECT COUNT(*) - COUNT(DISTINCT weather_date) FROM clean_weather",
    "temperature is realistic (-40 to 120 F)":
        "SELECT COUNT(*) FROM clean_weather WHERE temp_max_f NOT BETWEEN -40 AND 120",
    "rain is not negative":
        "SELECT COUNT(*) FROM clean_weather WHERE precip_in < 0",
    "wind gust is realistic (0 to 150 mph)":
        "SELECT COUNT(*) FROM clean_weather WHERE gust_max_mph NOT BETWEEN 0 AND 150",
    "data is fresh (loaded within 2 days)":
        """SELECT CASE WHEN MAX(weather_date) >= current_date - 2
                       THEN 0 ELSE 1 END FROM clean_weather""",
}

failed = 0
for name, sql in checks.items():
    bad = con.execute(sql).fetchone()[0]
    if bad == 0:
        print("PASS:", name)
    else:
        print("FAIL:", name, "-", bad, "bad")
        failed += 1

con.close()

if failed > 0:
    print(failed, "check(s) failed. Stopping the pipeline.")
    sys.exit(1)

print("All checks passed.")