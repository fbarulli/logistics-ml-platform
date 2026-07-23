import json
from pathlib import Path
from datetime import datetime

from logistics_ml.features.schema import (
    RAW_FEATURES,
    RAW_FEATURE_TYPES,
    STREAM_FEATURE_TYPES,
)


CONTRACT = Path("schemas/feature_contract.json")
FLINK_DIR = Path("flink/sql/generated")


TYPE_MAP = {
    int: {
        "logical": "int",
        "flink": "INT",
    },
    float: {
        "logical": "float",
        "flink": "DOUBLE",
    },
    datetime: {
        "logical": "datetime",
        "flink": "STRING",
    },
}


def feature_type(dtype):
    return TYPE_MAP[dtype]


def transform_expression(name):
    if name == "pickup_hour":
        return "CAST(EXTRACT(HOUR FROM CAST(pickup_datetime AS TIMESTAMP(3))) AS INT)"

    if name == "pickup_day_of_week":
        return "CAST(MOD(DAYOFWEEK(CAST(pickup_datetime AS TIMESTAMP(3))) + 5, 7) AS INT)"

    if name == "pickup_month":
        return "CAST(EXTRACT(MONTH FROM CAST(pickup_datetime AS TIMESTAMP(3))) AS INT)"

    return name


def main():
    FLINK_DIR.mkdir(parents=True, exist_ok=True)
    CONTRACT.parent.mkdir(exist_ok=True)

    contract = {
        "raw_features": [
            {
                "name": name,
                **feature_type(dtype),
            }
            for name, dtype in RAW_FEATURE_TYPES.items()
        ],
        "stream_features": [
            {
                "name": name,
                **feature_type(dtype),
            }
            for name, dtype in STREAM_FEATURE_TYPES.items()
        ],
        "required_order": RAW_FEATURES,
    }

    CONTRACT.write_text(
        json.dumps(contract, indent=2) + "\n"
    )

    raw_columns = ",\n    ".join(
        f"{name} {feature_type(dtype)['flink']}"
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
    'properties.group.id' = 'taxi-feature-pipeline',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
);
"""

    sink_columns = ",\n    ".join(
        f"{name} {feature_type(dtype)['flink']}"
        for name, dtype in STREAM_FEATURE_TYPES.items()
    )

    sink_sql = f"""CREATE TABLE taxi_features (
    trip_id STRING,
    {sink_columns}
)
WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-features',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);
"""

    transform_columns = ",\n    ".join(
        transform_expression(name)
        for name in STREAM_FEATURE_TYPES
    )

    transform_sql = f"""INSERT INTO taxi_features
SELECT
    trip_id,
    {transform_columns}
FROM taxi_trips;
"""

    (FLINK_DIR / "01-source.sql").write_text(source_sql)
    (FLINK_DIR / "02-sink.sql").write_text(sink_sql)
    (FLINK_DIR / "03-transform.sql").write_text(transform_sql)

    print("Generated feature contracts")


if __name__ == "__main__":
    main()
