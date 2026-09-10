import pandas as pd

# Load elevation and drainage data
elevation_df = pd.read_csv(
    "data/processed/chennai_zone_elevation.csv"
)

drainage_df = pd.read_csv(
    "data/prototype/drainage_data.csv"
)

# Merge both datasets
combined = pd.merge(
    elevation_df,
    drainage_df,
    on="zone"
)

# Ask user for simulated rainfall
rainfall_mm = float(
    input("Enter simulated rainfall in mm: ")
)

# Calculate effective drainage
combined["effective_drainage"] = (
    combined["drainage_capacity"]
    * (1 - combined["blockage_percent"] / 100)
)

# Rainfall factor
rain_factor = min(rainfall_mm / 50, 1)

# Drainage weakness
combined["drainage_factor"] = (
    1 - combined["effective_drainage"] / 100
).clip(0, 1)

# Terrain factor
combined["terrain_factor"] = (
    (25 - combined["elevation_m"]) / 25
).clip(0, 1)

# Blockage factor
combined["blockage_factor"] = (
    combined["blockage_percent"] / 100
).clip(0, 1)

# Combined vulnerability
combined["vulnerability"] = (
    combined["drainage_factor"] * 0.40
    + combined["terrain_factor"] * 0.35
    + combined["blockage_factor"] * 0.25
)

# Final simulated risk score
combined["risk_score"] = (
    rain_factor
    * combined["vulnerability"]
    * 100
)

combined["risk_score"] = (
    combined["risk_score"]
    .clip(0, 100)
    .round(2)
)

print()
print("FloodSense AI - What-If Flood Simulator")
print("----------------------------------------")
print("Simulated rainfall:", rainfall_mm, "mm")
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