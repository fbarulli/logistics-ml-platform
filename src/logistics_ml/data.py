import io

import pandas as pd

from logistics_ml.db import engine

TRAINING_COLUMNS = [
    "pickup_datetime",
    "passenger_count",
    "trip_distance",
    "pickup_location_id",
    "dropoff_location_id",
    "trip_duration_minutes",
]

TRAINING_DTYPES = {
    "passenger_count": "float32",
    "trip_distance": "float32",
    "pickup_location_id": "int16",
    "dropoff_location_id": "int16",
    "trip_duration_minutes": "float32",
}

PARSE_DATES = ["pickup_datetime"]


def load_training_data() -> pd.DataFrame:
    """
    Load the offline training dataset.

    Uses COPY ... TO STDOUT instead of a standard SELECT so Postgres
    streams rows as CSV directly, avoiding the Python row-tuple
    materialization step that a normal read_sql_query performs for
    every cell before pandas ever sees it. For large row counts
    (10M+), that intermediate step -- not the final DataFrame -- is
    what was driving memory usage far past what the actual data
    requires.
    """
    print("Loading training_data...")

    cols = ", ".join(TRAINING_COLUMNS)
    query = f"COPY (SELECT {cols} FROM training_data) TO STDOUT WITH (FORMAT CSV, HEADER)"

    raw_conn = engine.raw_connection()
    try:
        buf = io.BytesIO()
        with raw_conn.cursor() as cur:
            with cur.copy(query) as copy:
                for chunk in copy:
                    buf.write(bytes(chunk))
        buf.seek(0)
    finally:
        raw_conn.close()

    df = pd.read_csv(
        buf,
        parse_dates=PARSE_DATES,
        dtype={
            col: dtype
            for col, dtype in TRAINING_DTYPES.items()
        },
    )

    print(f"Loaded {len(df):,} rows")

    return df
