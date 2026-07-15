from pathlib import Path

import duckdb

RAW_DATA = Path("data/raw/yellow_tripdata_2024-01.parquet")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "deliveries.parquet"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

query = """
SELECT
    VendorID AS courier_company,

    tpep_pickup_datetime AS restaurant_ready_time,
    tpep_dropoff_datetime AS delivered_time,

    PULocationID AS restaurant_id,
    DOLocationID AS customer_id,

    trip_distance,

    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
    EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS pickup_day_of_week,
    EXTRACT(MONTH FROM tpep_pickup_datetime) AS pickup_month,

    CASE
        WHEN EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) IN (0, 6)
        THEN 1
        ELSE 0
    END AS is_weekend,

    DATE_DIFF(
        'minute',
        tpep_pickup_datetime,
        tpep_dropoff_datetime
    ) AS delivery_time_minutes

FROM read_parquet(?)

WHERE
    trip_distance > 0
    AND tpep_dropoff_datetime > tpep_pickup_datetime
    AND trip_distance < 50
    AND DATE_DIFF(
        'minute',
        tpep_pickup_datetime,
        tpep_dropoff_datetime
    ) BETWEEN 1 AND 180
"""

con = duckdb.connect()

con.execute(
    f"""
    COPY (
        {query}
    )
    TO '{OUTPUT_FILE}'
    (FORMAT PARQUET);
    """,
    [str(RAW_DATA)],
)

print(f"✅ Saved processed dataset to {OUTPUT_FILE}")

stats = con.execute(
    f"""
    SELECT
        COUNT(*) AS rows,
        AVG(delivery_time_minutes) AS avg_delivery_minutes,
        MIN(delivery_time_minutes) AS min_delivery_minutes,
        MAX(delivery_time_minutes) AS max_delivery_minutes,
        AVG(trip_distance) AS avg_trip_distance
    FROM read_parquet('{OUTPUT_FILE}')
    """
).fetchdf()

print("\nDataset summary:")
print(stats)

preview = con.execute(
    f"""
    SELECT *
    FROM read_parquet('{OUTPUT_FILE}')
    LIMIT 5
    """
).fetchdf()

print("\nPreview:")
print(preview)
