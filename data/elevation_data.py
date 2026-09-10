import requests
import pandas as pd

# Chennai prototype location
latitude = 13.0827
longitude = 80.2707

url = "https://api.open-meteo.com/v1/elevation"

params = {
    "latitude": latitude,
    "longitude": longitude
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    elevation = data["elevation"][0]

    elevation_df = pd.DataFrame({
        "latitude": [latitude],
        "longitude": [longitude],
        "elevation_m": [elevation]
    })

    elevation_df.to_csv(
        "data/raw/elevation_data.csv",
        index=False
    )

    print("Elevation data saved successfully.")
    print(elevation_df)

else:
    print("Unable to fetch elevation data.")