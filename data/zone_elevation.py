import requests
import pandas as pd

# Read prototype zone coordinates
zones = pd.read_csv("data/prototype/chennai_zones.csv")

elevations = []

for _, row in zones.iterrows():
    latitude = row["latitude"]
    longitude = row["longitude"]

    url = "https://api.open-meteo.com/v1/elevation"

    params = {
        "latitude": latitude,
        "longitude": longitude
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        elevation = data["elevation"][0]
    else:
        elevation = None

    elevations.append(elevation)

zones["elevation_m"] = elevations

zones.to_csv(
    "data/processed/chennai_zone_elevation.csv",
    index=False
)

print("Zone elevation data saved successfully.")
print(zones)