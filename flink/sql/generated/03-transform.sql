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
