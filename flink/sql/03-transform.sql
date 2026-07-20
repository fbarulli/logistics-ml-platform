INSERT INTO taxi_features
SELECT
    trip_id,
    pickup_zone,
    dropoff_zone,
    distance_km,
    passengers,
    EXTRACT(HOUR FROM CAST(event_time AS TIMESTAMP(3))),
    EXTRACT(DAY_OF_WEEK FROM CAST(event_time AS TIMESTAMP(3))),
    EXTRACT(MONTH FROM CAST(event_time AS TIMESTAMP(3)))
FROM taxi_trips;
