from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"
)

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

query = """
SELECT
    pickup_hour,
    pickup_day_of_week,
    pickup_month,
    passenger_count,
    trip_distance,
    pickup_location_id,
    dropoff_location_id,
    trip_duration_minutes,
    fare_amount
FROM training_data
"""

chunksize = 500_000

for i, chunk in enumerate(pd.read_sql(query, engine, chunksize=chunksize)):
    filename = output_dir / f"training_data_part_{i:02d}.parquet"
    chunk.to_parquet(filename, index=False)
    print(f"Wrote {filename} ({len(chunk):,} rows)")
