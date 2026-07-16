import pandas as pd

from logistics_ml.db import engine


def read_table(table_name: str) -> pd.DataFrame:
    print(f"Loading {table_name}...")

    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)

    print(f"Loaded {len(df):,} rows")

    return df


def load_training_data() -> pd.DataFrame:
    return read_table("training_data")
