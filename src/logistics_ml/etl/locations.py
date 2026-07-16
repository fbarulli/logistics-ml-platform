import pandas as pd

from logistics_ml.config import LOCATION_LOOKUP_FILE
from logistics_ml.db import engine


def load_locations():
    df = pd.read_csv(LOCATION_LOOKUP_FILE)

    df.columns = [
        "location_id",
        "borough",
        "zone",
        "service_zone",
    ]

    df.to_sql(
        "locations",
        engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df):,} locations")


def main():
    load_locations()


if __name__ == "__main__":
    main()
