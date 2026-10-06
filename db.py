import os
import duckdb

def connect():
    token = os.environ.get("MOTHERDUCK_TOKEN")
    if token:
        # Running in GitHub Actions: use the cloud database
        con = duckdb.connect(f"md:?motherduck_token={token}")
        con.execute("CREATE DATABASE IF NOT EXISTS weather")
        con.execute("USE weather")
        return con
    # Running in the Codespace: use the local file
    return duckdb.connect("weather.duckdb")