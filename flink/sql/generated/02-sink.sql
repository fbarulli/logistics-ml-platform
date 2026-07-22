CREATE TABLE taxi_features (
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
