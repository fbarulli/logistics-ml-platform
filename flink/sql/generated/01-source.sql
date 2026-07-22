CREATE TABLE taxi_trips (
    trip_id STRING,
    pickup_datetime STRING,
    passenger_count DOUBLE,
    trip_distance DOUBLE,
    pickup_location_id INT,
    dropoff_location_id INT
)
WITH (
    'connector' = 'kafka',
    'topic' = 'taxi-trips',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);
