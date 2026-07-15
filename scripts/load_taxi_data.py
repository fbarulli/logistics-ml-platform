from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm

DATABASE_URL = "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"

engine = create_engine(DATABASE_URL)

DATA_DIR = Path("data/raw")


def copy_chunk(df: pd.DataFrame) -> None:
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    conn = engine.raw_connection()
    try:
        cur = conn.cursor()

        with cur.copy(
            """
            COPY taxi_trips (
                vendor_id,
                pickup_datetime,
                dropoff_datetime,
                passenger_count,
                trip_distance,
                pickup_location_id,
                dropoff_location_id,
                fare_amount,
                tip_amount,
                total_amount
            )
            FROM STDIN WITH (FORMAT CSV)
            """
        ) as copy:
            while chunk := buffer.read(1024 * 1024):
                copy.write(chunk)

        conn.commit()

    finally:
        conn.close()


def main():
    print("Reading parquet...")

    df = pd.read_parquet(
        "data/raw/yellow_tripdata_2024-01.parquet",
        columns=[
            "VendorID",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "PULocationID",
            "DOLocationID",
            "fare_amount",
            "tip_amount",
            "total_amount",
        ],
    )

    df.columns = [
        "vendor_id",
        "pickup_datetime",
        "dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "pickup_location_id",
        "dropoff_location_id",
        "fare_amount",
        "tip_amount",
        "total_amount",
    ]

    chunk_size = 100000

    for start in tqdm(
        range(0, len(df), chunk_size),
        desc="yellow_tripdata_2024-01.parquet",
        unit="chunk",
    ):
        chunk = df.iloc[start:start + chunk_size].copy()

        # Convert nullable integer columns
        chunk["vendor_id"] = chunk["vendor_id"].astype("Int64")
        chunk["pickup_location_id"] = chunk["pickup_location_id"].astype(
            "Int64")
        chunk["dropoff_location_id"] = chunk["dropoff_location_id"].astype(
            "Int64")
        chunk["passenger_count"] = (
            chunk["passenger_count"]
            .fillna(0)
            .round()
            .astype("Int64")
        )

        copy_chunk(chunk)

    print("Done.")


if __name__ == "__main__":
    main()
