CREATE TABLE taxi_trips (
    trip_id STRING,
    pickup_zone INT,
    dropoff_zone INT,
    distance_km DOUBLE,
    passengers INT,
    event_time TIMESTAMP(3),

    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-trips',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-taxi',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
);


CREATE TABLE taxi_features (
    trip_id STRING,
    pickup_zone INT,
    dropoff_zone INT,
    distance_km DOUBLE,
    passengers INT,

    pickup_hour INT,
    pickup_day_of_week INT,
    pickup_month INT
) WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-features',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);


INSERT INTO taxi_features
SELECT
    trip_id,
    pickup_zone,
    dropoff_zone,
    distance_km,
    passengers,

    HOUR(event_time),
    DAYOFWEEK(event_time),
    MONTH(event_time)

FROM taxi_trips;
