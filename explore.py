import glob
import pandas as pd
import glob
import pandas as pd

# ---- Load the raw data ----
flight_csv_file = glob.glob("data/*.csv")[0]
print(f"Loading file: {flight_csv_file}\n")

all_us_flights = pd.read_csv(flight_csv_file, low_memory=False)
total_rows, total_columns = all_us_flights.shape
print(f"All US flights: {total_rows:,} rows, {total_columns} columns")

# ---- Keep only flights departing from or arriving at MCO ----
departs_mco = all_us_flights["Origin"] == "MCO"
arrives_mco = all_us_flights["Dest"] == "MCO"
mco_flights = all_us_flights[departs_mco | arrives_mco]
print(f"MCO flights:    {len(mco_flights):,} rows\n")

# ---- Preview the columns we care about ----
preview_columns = [
    "FlightDate", "Reporting_Airline", "Origin", "Dest",
    "CRSDepTime", "DepDelay", "ArrDelay", "Cancelled", "Diverted",
]
print("=== Sample of 10 MCO flights ===")
print(mco_flights[preview_columns].head(10))

# ---- Average arrival delay by airline (minutes, negative = early) ----
avg_arrival_delay_by_airline = (
    mco_flights
    .groupby("Reporting_Airline")["ArrDelay"]
    .mean()
    .round(1)
    .sort_values()
)
print("\n=== Average arrival delay at MCO by airline (minutes) ===")
print(avg_arrival_delay_by_airline.to_string())