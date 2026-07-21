#/workspace/docker/postgres/init.sql
CREATE DATABASE mlflow;

\connect logistics

CREATE TABLE IF NOT EXISTS taxi_predictions (
    id SERIAL PRIMARY KEY,
    trip_id TEXT NOT NULL,
    prediction DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS taxi_trips (
    vendorid INT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count DOUBLE PRECISION,
    trip_distance DOUBLE PRECISION,
    ratecodeid DOUBLE PRECISION,
    store_and_fwd_flag TEXT,
    pickup_location_id INT,
    dropoff_location_id INT,
    payment_type BIGINT,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    congestion_surcharge DOUBLE PRECISION,
    airport_fee DOUBLE PRECISION
);
