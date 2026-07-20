CREATE TABLE taxi_trips (
    trip_id STRING,
    pickup_zone INT,
    dropoff_zone INT,
    distance_km DOUBLE,
    passengers INT,
    event_time STRING
)
WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-trips',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-features',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
);
