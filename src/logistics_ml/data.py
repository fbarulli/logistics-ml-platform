import pandas as pd

from logistics_ml.db import engine


def read_table(table_name: str) -> pd.DataFrame:
    """
    Read an entire table from PostgreSQL.
    """

    print(f"Loading {table_name}...")

    df = pd.read_sql_table(table_name, engine)

    print(f"Loaded {len(df):,} rows")

    return df


def load_training_data() -> pd.DataFrame:
    """
    Load the offline training dataset.
    """

    return read_table("training_data")
