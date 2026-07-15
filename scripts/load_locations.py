import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"
)

FILE = "data/raw/taxi_zone_lookup.csv"


def main():
    engine = create_engine(DATABASE_URL)

    df = pd.read_csv(FILE)

    df.columns = [
        "location_id",
        "borough",
        "zone",
        "service_zone",
    ]

    df.to_sql(
        "locations",
        engine,
        if_exists="append",
        index=False,
    )

    print("locations loaded:", len(df))


if __name__ == "__main__":
    main()
