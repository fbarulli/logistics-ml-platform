# src/logistics_ml/config.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://logistics:logistics@postgres:5432/logistics",
)

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow:5000",
)

RANDOM_STATE = 42

FEATURES = [
    "passenger_count",
    "pickup_location_id",
    "dropoff_location_id",
    "pickup_hour",
    "pickup_day_of_week",
    "pickup_month",
    "trip_distance",
]

TARGET = "trip_duration_minutes"

from pathlib import Path

RAW_DATA_URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    "trip-data/yellow_tripdata_2024-01.parquet"
)

DATA_DIR = Path("data/raw")
RAW_DATA_FILE = DATA_DIR / "yellow_tripdata_2024-01.parquet"

LOCATION_LOOKUP_FILE = "data/raw/taxi_zone_lookup.csv"
