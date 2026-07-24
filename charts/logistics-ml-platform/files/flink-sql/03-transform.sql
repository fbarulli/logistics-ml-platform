INSERT INTO taxi_features
SELECT
    trip_id,
    pickup_location_id,
    dropoff_location_id,
    trip_distance,
    passenger_count,
    CAST(EXTRACT(HOUR FROM CAST(pickup_datetime AS TIMESTAMP(3))) AS INT),
    CAST(MOD(DAYOFWEEK(CAST(pickup_datetime AS TIMESTAMP(3))) + 5, 7) AS INT),
    CAST(EXTRACT(MONTH FROM CAST(pickup_datetime AS TIMESTAMP(3))) AS INT)
FROM taxi_trips;
