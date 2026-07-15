import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"
)

PARQUET_FILE = "data/raw/yellow_tripdata_2024-01.parquet"


def main():
    engine = create_engine(DATABASE_URL)

    print("Loading parquet...")
    df = pd.read_parquet(PARQUET_FILE)

    print(df.head())
    print(df.shape)

    df = df.rename(
        columns={
            "VendorID": "vendor_id",
            "tpep_pickup_datetime": "pickup_datetime",
            "tpep_dropoff_datetime": "dropoff_datetime",
            "passenger_count": "passenger_count",
            "trip_distance": "trip_distance",
            "PULocationID": "pickup_location_id",
            "DOLocationID": "dropoff_location_id",
            "fare_amount": "fare_amount",
            "tip_amount": "tip_amount",
            "total_amount": "total_amount",
        }
    )

    columns = [
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

    df = df[columns]

    print("Writing to PostgreSQL...")

    df.to_sql(
        "taxi_trips",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )

    print("Done.")


if __name__ == "__main__":
    main()
