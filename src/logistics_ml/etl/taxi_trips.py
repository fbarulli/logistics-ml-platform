from pathlib import Path

import pandas as pd

from logistics_ml.db import engine


FILE = Path("data/raw/yellow_tripdata_2024-01.parquet")


def load_taxi_trips():
    print("Loading taxi trips...")

    df = pd.read_parquet(FILE)
    df.columns = [c.lower() for c in df.columns]

    df = df.rename(columns={
        "pulocationid": "pickup_location_id",
        "dolocationid": "dropoff_location_id",
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
    })

    df.to_sql(
        "taxi_trips",
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
    )

    print(f"Loaded taxi_trips: {len(df):,} rows")
