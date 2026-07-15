import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATABASE_URL = "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"

engine = create_engine(DATABASE_URL)

query = """
SELECT
    trip_distance,
    passenger_count,
    EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
    pickup_location_id,
    dropoff_location_id,
    total_amount
FROM taxi_trips
WHERE total_amount > 0
"""

df = pd.read_sql(query, engine)

X = df[
    [
        "trip_distance",
        "passenger_count",
        "pickup_hour",
        "pickup_location_id",
        "dropoff_location_id",
    ]
]

y = df["total_amount"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(f"MAE : {mean_absolute_error(y_test, predictions):.2f}")
print(f"RMSE: {mean_squared_error(y_test, predictions) ** 0.5:.2f}")
print(f"R²  : {r2_score(y_test, predictions):.4f}")
