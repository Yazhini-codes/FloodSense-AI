import pandas as pd


# ============================================================
# FLOODSENSE AI - PROTOTYPE CONFIGURATION
# ============================================================

# True = use a simulated heavy-rain condition for SIH demo
# False = use rainfall directly from rainfall_data.csv
USE_PROTOTYPE_SCENARIO = False

# Prototype rainfall intensity used only when scenario mode is ON
PROTOTYPE_RAINFALL_MM = 60.0


# ============================================================
# LOAD DATA
# ============================================================

elevation_df = pd.read_csv(
    "data/processed/chennai_zone_elevation.csv"
)

drainage_df = pd.read_csv(
    "data/prototype/drainage_data.csv"
)

rainfall_df = pd.read_csv(
    "data/raw/rainfall_data.csv"
)

nowcast_rainfall_df = pd.read_csv(
    "data/raw/nowcast_rainfall.csv"
)


# ============================================================
# RAINFALL INPUT
# ============================================================

actual_rainfall_mm = rainfall_df["rainfall_mm"].max()


if USE_PROTOTYPE_SCENARIO:

    rainfall_mm = PROTOTYPE_RAINFALL_MM

    rainfall_mode = "PROTOTYPE HEAVY RAIN SCENARIO"

else:

    rainfall_mm = actual_rainfall_mm

    rainfall_mode = "DATASET RAINFALL"


# ============================================================
# MERGE ELEVATION + DRAINAGE
# ============================================================

combined = pd.merge(
    elevation_df,
    drainage_df,
    on="zone"
)


# ============================================================
# EFFECTIVE DRAINAGE
# ============================================================

combined["effective_drainage"] = (
    combined["drainage_capacity"]
    * (
        1 -
        combined["blockage_percent"] / 100
    )
)


# ============================================================
# DRAINAGE WEAKNESS
# ============================================================

combined["drainage_factor"] = (
    1 -
    combined["effective_drainage"] / 100
).clip(
    0,
    1
)


# ============================================================
# TERRAIN / ELEVATION FACTOR
# ============================================================

combined["terrain_factor"] = (
    (
        25 -
        combined["elevation_m"]
    )
    / 25
).clip(
    0,
    1
)


# ============================================================
# BLOCKAGE FACTOR
# ============================================================

combined["blockage_factor"] = (
    combined["blockage_percent"]
    / 100
).clip(
    0,
    1
)


# ============================================================
# OVERALL VULNERABILITY
# ============================================================

combined["vulnerability"] = (

    combined["drainage_factor"] * 0.40

    +

    combined["terrain_factor"] * 0.35

    +

    combined["blockage_factor"] * 0.25

)


# ============================================================
# RISK CATEGORY FUNCTION
# ============================================================

def get_risk_level(score):

    if score < 25:

        return "LOW"

    elif score < 50:

        return "MODERATE"

    elif score < 75:

        return "HIGH"

    else:

        return "CRITICAL"


# ============================================================
# CURRENT FLOOD RISK
# ============================================================

rain_factor = min(
    rainfall_mm / 50,
    1
)


combined["risk_score"] = (

    rain_factor

    *

    combined["vulnerability"]

    *

    100

).clip(
    0,
    100
).round(2)


combined["risk_level"] = (
    combined["risk_score"]
    .apply(get_risk_level)
)


# ============================================================
# ADD CURRENT-RISK METADATA
# ============================================================

combined["actual_dataset_rainfall_mm"] = (
    actual_rainfall_mm
)

combined["rainfall_used_mm"] = (
    rainfall_mm
)

combined["rainfall_mode"] = (
    rainfall_mode
)


# ============================================================
# SAVE CURRENT FLOOD-RISK DATA
# ============================================================

combined.to_csv(
    "data/processed/final_risk_data.csv",
    index=False
)


# ============================================================
# 0-3 HOUR FLOOD-RISK NOWCAST
# ============================================================

nowcast_results = []


for _, rain_row in nowcast_rainfall_df.iterrows():

    forecast_period = rain_row["forecast_period"]

    forecast_time = rain_row["time"]

    forecast_rainfall = float(
        rain_row["rainfall_mm"]
    )


    # --------------------------------------------
    # Convert rainfall to rainfall severity factor
    # --------------------------------------------

    forecast_rain_factor = min(
        forecast_rainfall / 50,
        1
    )


    # --------------------------------------------
    # Calculate risk for every zone
    # --------------------------------------------

    for _, zone_row in combined.iterrows():

        forecast_risk = (

            forecast_rain_factor

            *

            zone_row["vulnerability"]

            *

            100

        )


        forecast_risk = max(
            0,
            min(
                forecast_risk,
                100
            )
        )


        forecast_risk = round(
            forecast_risk,
            2
        )


        forecast_level = get_risk_level(
            forecast_risk
        )


        nowcast_results.append(
            {
                "forecast_period":
                    forecast_period,

                "time":
                    forecast_time,

                "zone":
                    zone_row["zone"],

                "rainfall_mm":
                    forecast_rainfall,

                "elevation_m":
                    zone_row["elevation_m"],

                "effective_drainage":
                    zone_row["effective_drainage"],

                "blockage_percent":
                    zone_row["blockage_percent"],

                "vulnerability":
                    round(
                        zone_row["vulnerability"],
                        4
                    ),

                "risk_score":
                    forecast_risk,

                "risk_level":
                    forecast_level
            }
        )


# ============================================================
# SAVE 0-3 HOUR FLOOD-RISK NOWCAST
# ============================================================

nowcast_risk_df = pd.DataFrame(
    nowcast_results
)


nowcast_risk_df.to_csv(
    "data/processed/nowcast_risk_data.csv",
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()

print(
    "=============================================="
)

print(
    "       FloodSense AI - Final Risk Engine"
)

print(
    "=============================================="
)

print()

print(
    "Actual dataset rainfall:",
    actual_rainfall_mm,
    "mm"
)

print(
    "Rainfall used for current calculation:",
    rainfall_mm,
    "mm"
)

print(
    "Mode:",
    rainfall_mode
)

print()

print(
    "CURRENT ZONE-WISE FLOOD RISK"
)

print()

print(
    combined[
        [
            "zone",
            "elevation_m",
            "effective_drainage",
            "blockage_percent",
            "risk_score",
            "risk_level"
        ]
    ]
)

print()

print(
    "=============================================="
)

print(
    "       0-3 HOUR FLOOD-RISK NOWCAST"
)

print(
    "=============================================="
)

print()

print(
    nowcast_risk_df[
        [
            "forecast_period",
            "time",
            "zone",
            "rainfall_mm",
            "risk_score",
            "risk_level"
        ]
    ].to_string(
        index=False
    )
)

print()

print(
    "Current flood risk saved to:"
)

print(
    "data/processed/final_risk_data.csv"
)

print()

print(
    "0-3 hour flood-risk nowcast saved to:"
)

print(
    "data/processed/nowcast_risk_data.csv"
)

print()