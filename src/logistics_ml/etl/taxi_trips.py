from pathlib import Path
import io
import time
import pyarrow.parquet as pq
from tqdm import tqdm
from logistics_ml.db import engine

RAW_DIR = Path("data/raw")

RENAME = {
    "pulocationid": "pickup_location_id",
    "dolocationid": "dropoff_location_id",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
}
BATCH_SIZE = 200_000


def load_taxi_trips():
    files = sorted(RAW_DIR.glob("yellow_tripdata_*.parquet"))
    print("Loading taxi trips...")
    print(f"Found {len(files)} files: {[f.name for f in files]}")
    total_rows = 0
    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE taxi_trips")
        existing_cols = [
            row[0] for row in conn.exec_driver_sql(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'taxi_trips'"
            )
        ]
    raw_conn = engine.raw_connection()
    try:
        for f in tqdm(files, desc="Files"):
            start = time.time()
            file_rows = 0
            parquet_file = pq.ParquetFile(f)
            for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
                part = batch.to_pandas()
                part.columns = [c.lower() for c in part.columns]
                part = part.rename(columns=RENAME)
                part = part[[c for c in part.columns if c in existing_cols]]
                buf = io.StringIO()
                part.to_csv(buf, index=False, header=False)
                buf.seek(0)
                with raw_conn.cursor() as cur:
                    cols = ",".join(part.columns)
                    with cur.copy(
                        f"COPY taxi_trips ({cols}) FROM STDIN WITH (FORMAT CSV)"
                    ) as copy:
                        copy.write(buf.read())
                raw_conn.commit()
                file_rows += len(part)
            total_rows += file_rows
            print(f"  {f.name}: {file_rows:,} rows in {time.time() - start:.1f}s")
    finally:
        raw_conn.close()
    print(f"Loaded taxi_trips: {total_rows:,} rows")
