import pandas as pd

# Load processed elevation data
elevation_df = pd.read_csv(
    "data/processed/chennai_zone_elevation.csv"
)

# Load prototype drainage data
drainage_df = pd.read_csv(
    "data/prototype/drainage_data.csv"
)

# Load rainfall data
rainfall_df = pd.read_csv(
    "data/raw/rainfall_data.csv"
)

# Use the highest forecast rainfall value for now
current_rainfall = rainfall_df["rainfall_mm"].max()

# Combine elevation + drainage data using zone name
combined = pd.merge(
    elevation_df,
    drainage_df,
    on="zone"
)

# Calculate effective drainage after blockage
combined["effective_drainage"] = (
    combined["drainage_capacity"]
    * (1 - combined["blockage_percent"] / 100)
)

# Simple prototype risk score
combined["risk_score"] = (
    current_rainfall * 4
    + combined["blockage_percent"] * 1.2
    + (25 - combined["elevation_m"]) * 1.5
    + (100 - combined["effective_drainage"]) * 0.5
)

# Keep score between 0 and 100
combined["risk_score"] = combined["risk_score"].clip(0, 100)

print("FloodSense AI - Flood Risk Engine")
print("---------------------------------")
print("Rainfall used:", current_rainfall, "mm")
print()

print(
    combined[
        [
            "zone",
            "elevation_m",
            "effective_drainage",
            "blockage_percent",
            "risk_score"
        ]
    ]
)