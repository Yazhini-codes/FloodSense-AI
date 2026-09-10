import pandas as pd

# Load data
elevation_df = pd.read_csv(
    "data/processed/chennai_zone_elevation.csv"
)

drainage_df = pd.read_csv(
    "data/prototype/drainage_data.csv"
)

rainfall_df = pd.read_csv(
    "data/raw/rainfall_data.csv"
)

# Highest forecast rainfall for the day
rainfall_mm = rainfall_df["rainfall_mm"].max()

# Merge elevation + drainage data
combined = pd.merge(
    elevation_df,
    drainage_df,
    on="zone"
)

# Effective drainage after blockage
combined["effective_drainage"] = (
    combined["drainage_capacity"]
    * (1 - combined["blockage_percent"] / 100)
)

# -----------------------------
# Improved prototype risk model
# -----------------------------

# Rainfall factor: 0 to 1
rain_factor = min(rainfall_mm / 50, 1)

# Drainage weakness: 0 to 1
combined["drainage_factor"] = (
    1 - combined["effective_drainage"] / 100
).clip(0, 1)

# Lower elevation = higher terrain risk
combined["terrain_factor"] = (
    (25 - combined["elevation_m"]) / 25
).clip(0, 1)

# Blockage factor: 0 to 1
combined["blockage_factor"] = (
    combined["blockage_percent"] / 100
).clip(0, 1)

# Combined vulnerability
combined["vulnerability"] = (
    combined["drainage_factor"] * 0.40
    + combined["terrain_factor"] * 0.35
    + combined["blockage_factor"] * 0.25
)

# Final flood risk
# Rainfall acts as the trigger
combined["risk_score"] = (
    rain_factor
    * combined["vulnerability"]
    * 100
)

combined["risk_score"] = combined["risk_score"].clip(0, 100)

print("FloodSense AI - Improved Flood Risk Engine")
print("-------------------------------------------")
print("Rainfall used:", rainfall_mm, "mm")
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