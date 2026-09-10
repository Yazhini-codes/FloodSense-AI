from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd


app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ============================================================
# ZONE-WISE CURRENT FLOOD RISK API
# ============================================================

@app.get("/api/zones")
def get_zones():

    df = pd.read_csv(
        "data/processed/final_risk_data.csv"
    )

    zone_data = []

    for _, row in df.iterrows():

        zone_data.append(
            {
                "zone":
                    row["zone"],

                "elevation_m":
                    float(
                        row["elevation_m"]
                    ),

                "terrain_factor":
                    float(
                        row["terrain_factor"]
                    ),

                "effective_drainage":
                    float(
                        row["effective_drainage"]
                    ),

                "blockage_percent":
                    float(
                        row["blockage_percent"]
                    ),

                "vulnerability":
                    float(
                        row["vulnerability"]
                    ),

                "risk_score":
                    float(
                        row["risk_score"]
                    ),

                "risk_level":
                    row["risk_level"],

                "actual_rainfall_mm":
                    float(
                        row["actual_dataset_rainfall_mm"]
                    ),

                "rainfall_used_mm":
                    float(
                        row["rainfall_used_mm"]
                    ),

                "rainfall_mode":
                    row["rainfall_mode"]
            }
        )

    return zone_data


# ============================================================
# 0-3 HOUR RAINFALL NOWCAST API
# ============================================================

@app.get("/api/nowcast")
def get_nowcast():

    df = pd.read_csv(
        "data/raw/nowcast_rainfall.csv"
    )

    nowcast_data = []

    for _, row in df.iterrows():

        nowcast_data.append(
            {
                "forecast_period":
                    row["forecast_period"],

                "time":
                    str(
                        row["time"]
                    ),

                "rainfall_mm":
                    float(
                        row["rainfall_mm"]
                    )
            }
        )

    return nowcast_data


# ============================================================
# 0-3 HOUR FLOOD-RISK NOWCAST API
# ============================================================

@app.get("/api/risk-nowcast")
def get_risk_nowcast():

    df = pd.read_csv(
        "data/processed/nowcast_risk_data.csv"
    )

    risk_nowcast_data = []

    for _, row in df.iterrows():

        risk_nowcast_data.append(
            {
                "forecast_period":
                    row["forecast_period"],

                "time":
                    str(
                        row["time"]
                    ),

                "zone":
                    row["zone"],

                "rainfall_mm":
                    float(
                        row["rainfall_mm"]
                    ),

                "elevation_m":
                    float(
                        row["elevation_m"]
                    ),

                "effective_drainage":
                    float(
                        row["effective_drainage"]
                    ),

                "blockage_percent":
                    float(
                        row["blockage_percent"]
                    ),

                "vulnerability":
                    float(
                        row["vulnerability"]
                    ),

                "risk_score":
                    float(
                        row["risk_score"]
                    ),

                "risk_level":
                    row["risk_level"]
            }
        )

    return risk_nowcast_data