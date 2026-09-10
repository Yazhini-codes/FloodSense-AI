import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# FLOODSENSE AI - WEATHER / RAINFALL NOWCAST
# ============================================================

# Chennai coordinates
latitude = 13.0827
longitude = 80.2707


# ============================================================
# OPEN-METEO API
# ============================================================

url = "https://api.open-meteo.com/v1/forecast"

params = {

    "latitude": latitude,

    "longitude": longitude,

    "hourly": "precipitation",

    # 2 days are requested so that
    # late-night forecasts can continue past midnight
    "forecast_days": 2,

    "timezone": "Asia/Kolkata"

}


# ============================================================
# FETCH WEATHER DATA
# ============================================================

response = requests.get(
    url,
    params=params,
    timeout=20
)


# ============================================================
# PROCESS RESPONSE
# ============================================================

if response.status_code == 200:

    data = response.json()

    times = data["hourly"]["time"]

    rainfall = data["hourly"]["precipitation"]


    # --------------------------------------------------------
    # COMPLETE HOURLY RAINFALL DATA
    # --------------------------------------------------------

    rainfall_df = pd.DataFrame({

        "time": times,

        "rainfall_mm": rainfall

    })


    rainfall_df["time"] = pd.to_datetime(
        rainfall_df["time"]
    )


    # Save complete forecast data
    rainfall_df.to_csv(

        "data/raw/rainfall_data.csv",

        index=False

    )


    # ========================================================
    # CREATE 0-3 HOUR NOWCAST
    # ========================================================

    # Current Chennai time
    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    # Convert to current hour
    current_hour = pd.Timestamp(
        current_time.replace(
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=None
        )
    )


    # Select current hour and future hours
    future_rainfall = rainfall_df[

        rainfall_df["time"] >= current_hour

    ].copy()


    # Take only:
    # NOW, +1 hour, +2 hours, +3 hours
    nowcast_df = future_rainfall.head(4).copy()


    # Add forecast labels
    labels = [
        "NOW",
        "+1 HOUR",
        "+2 HOURS",
        "+3 HOURS"
    ]


    nowcast_df["forecast_period"] = labels[
        :len(nowcast_df)
    ]


    # Arrange columns
    nowcast_df = nowcast_df[

        [
            "forecast_period",
            "time",
            "rainfall_mm"
        ]

    ]


    # Save 0-3 hour rainfall nowcast
    nowcast_df.to_csv(

        "data/raw/nowcast_rainfall.csv",

        index=False

    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    print()

    print(
        "=============================================="
    )

    print(
        "     FloodSense AI - Rainfall Nowcast"
    )

    print(
        "=============================================="
    )

    print()

    print(
        "Weather data fetched successfully."
    )

    print()

    print(
        "Current Chennai time:",
        current_time.strftime(
            "%Y-%m-%d %H:%M"
        )
    )

    print()

    print(
        "0-3 Hour Rainfall Forecast:"
    )

    print()

    print(
        nowcast_df.to_string(
            index=False
        )
    )

    print()

    print(
        "Complete rainfall data saved to:"
    )

    print(
        "data/raw/rainfall_data.csv"
    )

    print()

    print(
        "0-3 hour nowcast saved to:"
    )

    print(
        "data/raw/nowcast_rainfall.csv"
    )

    print()


# ============================================================
# ERROR
# ============================================================

else:

    print(
        "Unable to fetch weather data."
    )

    print(
        "HTTP Status:",
        response.status_code
    )