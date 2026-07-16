import mlflow
import pandas as pd

from logistics_ml.config import MLFLOW_TRACKING_URI


MODEL_NAME = "taxi-duration-model"


def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    return mlflow.pyfunc.load_model(
        f"models:/{MODEL_NAME}/latest"
    )


model = load_model()


def predict(payload: dict):
    df = pd.DataFrame([payload])

    prediction = model.predict(df)

    return {
        "trip_duration_minutes": float(prediction[0])
    }
