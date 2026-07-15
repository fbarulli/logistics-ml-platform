from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"
)

sql = """
CREATE OR REPLACE VIEW training_data AS
SELECT
    id,

    pickup_datetime,
    dropoff_datetime,

    EXTRACT(HOUR FROM pickup_datetime)      AS pickup_hour,
    EXTRACT(DOW FROM pickup_datetime)       AS pickup_day_of_week,
    EXTRACT(MONTH FROM pickup_datetime)     AS pickup_month,

    passenger_count,
    trip_distance,

    pickup_location_id,
    dropoff_location_id,

    fare_amount,
    tip_amount,

    total_amount,

    EXTRACT(EPOCH FROM (
        dropoff_datetime - pickup_datetime
    )) / 60.0 AS trip_duration_minutes

FROM taxi_trips;
"""

with engine.begin() as conn:
    conn.execute(text(sql))

print("training_data view created.")
