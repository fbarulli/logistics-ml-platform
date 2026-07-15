import duckdb
import pandas as pd

df = duckdb.sql("""
SELECT *
FROM 'data/raw/yellow_tripdata_2024-01.parquet'
LIMIT 10
""").to_df()

print(df.head())
print(df.columns)
