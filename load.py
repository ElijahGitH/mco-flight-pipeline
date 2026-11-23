import glob
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

# ---- Connect to the database (password comes from .env) ----
load_dotenv()
database = create_engine(os.environ["DATABASE_URL"])

AIRLINE_NAMES = {
    "AA": "American Airlines", "AS": "Alaska Airlines", "B6": "JetBlue",
    "DL": "Delta Air Lines", "F9": "Frontier", "G4": "Allegiant Air",
    "NK": "Spirit Airlines", "UA": "United Airlines", "WN": "Southwest",
    "OO": "SkyWest", "YX": "Republic Airways", "MQ": "Envoy Air",
    "9E": "Endeavor Air", "OH": "PSA Airlines", "HA": "Hawaiian Airlines",
}


def insert_skip_duplicates(table, connection, column_names, rows):
    """Insert rows, silently skipping any that already exist,
    so the script is safe to run more than once."""
    records = [dict(zip(column_names, row)) for row in rows]
    statement = insert(table.table).values(records).on_conflict_do_nothing()
    return connection.execute(statement).rowcount


def load_table(dataframe, table_name):
    # Turn pandas' NaN (missing values) into real database NULLs
    dataframe = dataframe.astype(object).where(dataframe.notna(), None)
    dataframe.to_sql(table_name, database, if_exists="append", index=False,
                     method=insert_skip_duplicates, chunksize=1000)
    print(f"Loaded {len(dataframe):,} rows into '{table_name}'")


# ---- EXTRACT: read the raw CSV ----
flight_csv_file = glob.glob("data/*.csv")[0]
print(f"Reading: {flight_csv_file}")
all_us_flights = pd.read_csv(flight_csv_file, low_memory=False)

# ---- TRANSFORM: keep MCO flights, rename columns to match our schema ----
mco = all_us_flights[(all_us_flights["Origin"] == "MCO") |
                     (all_us_flights["Dest"] == "MCO")]

airlines = pd.DataFrame({"airline_code": mco["Reporting_Airline"].unique()})
airlines["airline_name"] = airlines["airline_code"].map(AIRLINE_NAMES)

origin_airports = mco[["Origin", "OriginCityName", "OriginState"]]
origin_airports.columns = ["airport_code", "city", "state"]
dest_airports = mco[["Dest", "DestCityName", "DestState"]]
dest_airports.columns = ["airport_code", "city", "state"]
airports = pd.concat([origin_airports, dest_airports]).drop_duplicates("airport_code")
airports["city"] = airports["city"].str.split(",").str[0]  # "Orlando, FL" -> "Orlando"

flights = pd.DataFrame({
    "flight_date":         pd.to_datetime(mco["FlightDate"]).dt.date,
    "airline_code":        mco["Reporting_Airline"],
    "flight_number":       mco["Flight_Number_Reporting_Airline"],
    "origin":              mco["Origin"],
    "dest":                mco["Dest"],
    "sched_dep_time":      mco["CRSDepTime"],
    "dep_delay_min":       mco["DepDelay"],
    "arr_delay_min":       mco["ArrDelay"],
    "cancelled":           mco["Cancelled"] == 1,
    "diverted":            mco["Diverted"] == 1,
    "carrier_delay":       mco["CarrierDelay"],
    "weather_delay":       mco["WeatherDelay"],
    "nas_delay":           mco["NASDelay"],
    "security_delay":      mco["SecurityDelay"],
    "late_aircraft_delay": mco["LateAircraftDelay"],
})

# ---- LOAD: parent tables first, then flights (which references them) ----
load_table(airlines, "airlines")
load_table(airports, "airports")
load_table(flights, "flights")
print("Done!")