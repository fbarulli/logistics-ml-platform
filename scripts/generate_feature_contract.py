import json
from pathlib import Path

from logistics_ml.features.schema import RAW_FEATURES, RAW_FEATURE_TYPES


CONTRACT = Path("schemas/feature_contract.json")
FLINK_DIR = Path("flink/sql/generated")


def flink_type(py_type):
    mapping = {
        "<class 'int'>": "INT",
        "<class 'float'>": "DOUBLE",
        "<class 'str'>": "STRING",
        "<class 'datetime.datetime'>": "STRING",
    }
    return mapping[str(py_type)]


def main():
    FLINK_DIR.mkdir(parents=True, exist_ok=True)
    CONTRACT.parent.mkdir(exist_ok=True)

    contract = {
        "raw_features": [
            {
                "name": name,
                "type": str(dtype),
            }
            for name, dtype in RAW_FEATURE_TYPES.items()
        ],
        "required_order": RAW_FEATURES,
    }

    CONTRACT.write_text(
        json.dumps(contract, indent=2) + "\n"
    )

    raw_columns = ",\n    ".join(
        f"{name} {flink_type(dtype)}"
        for name, dtype in RAW_FEATURE_TYPES.items()
    )

    source_sql = f"""CREATE TABLE taxi_trips (
    trip_id STRING,
    {raw_columns}
)
WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-trips',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);
"""

    sink_sql = """CREATE TABLE taxi_features (
    trip_id STRING,
    pickup_location_id INT,
    dropoff_location_id INT,
    trip_distance DOUBLE,
    passenger_count INT,
    pickup_hour INT,
    pickup_day_of_week INT,
    pickup_month INT
)
WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-features',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);
"""

    transform_sql = """
INSERT INTO taxi_features
SELECT
    trip_id,
    pickup_location_id,
    dropoff_location_id,
    trip_distance,
    passenger_count,
    EXTRACT(HOUR FROM CAST(pickup_datetime AS TIMESTAMP(3))),
    EXTRACT(DAY_OF_WEEK FROM CAST(pickup_datetime AS TIMESTAMP(3))),
    EXTRACT(MONTH FROM CAST(pickup_datetime AS TIMESTAMP(3)))
FROM taxi_trips;
"""

    (FLINK_DIR / "01-source.sql").write_text(source_sql)
    (FLINK_DIR / "02-sink.sql").write_text(sink_sql)
    (FLINK_DIR / "03-transform.sql").write_text(transform_sql)

    print("Generated feature contracts")


if __name__ == "__main__":
    main()
