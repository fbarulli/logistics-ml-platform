CREATE DATABASE logistics;

CREATE DATABASE mlflow;

\connect logistics

CREATE TABLE IF NOT EXISTS taxi_predictions (
    id SERIAL PRIMARY KEY,
    trip_id TEXT NOT NULL,
    prediction DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
