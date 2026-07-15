from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"
)

df = pd.read_sql("SELECT * FROM taxi_trips", engine)

print("=" * 60)
print(f"Rows: {len(df):,}")
print("=" * 60)

print("\nMissing values")
print(df.isna().sum())

print("\nNumeric summary")
print(df.describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99]).T)

print("\nNegative values")
for col in [
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
]:
    print(f"{col}: {(df[col] < 0).sum():,}")
