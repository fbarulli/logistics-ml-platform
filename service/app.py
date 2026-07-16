from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import pandas as pd
import os

app = FastAPI()

MODEL_NAME = "taxi-duration-model"
MODEL_VERSION = "2"

model = None


class TaxiTrip(BaseModel):
    pickup_hour: int
    pickup_day_of_week: int
    pickup_month: int
    passenger_count: float
    trip_distance: float
    pickup_location_id: int
    dropoff_location_id: int
    fare_amount: float
    tip_amount: float
    total_amount: float


def get_model():
    global model

    if model is None:
        print("=== LOADING MODEL ===")

        tracking_uri = os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://mlflow:5000"
        )

        print("MLFLOW URI:")
        print(tracking_uri)

        mlflow.set_tracking_uri(tracking_uri)

        model_uri = "runs:/e8c184dbb671420e8e1fcad47b934889/model"

        print("MODEL URI:")
        print(model_uri)

        model = mlflow.pyfunc.load_model(model_uri)

        print("MODEL LOADED")

    return model


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/model")
def model_info():
    return {
        "model": MODEL_NAME,
        "version": MODEL_VERSION
    }


@app.post("/predict")
def predict(trip: TaxiTrip):

    print("=== PREDICT REQUEST ===")

    model = get_model()

    data = pd.DataFrame(
        [
            trip.model_dump()
        ]
    )

    prediction = model.predict(data)

    return {
        "prediction": float(prediction[0])
    }
