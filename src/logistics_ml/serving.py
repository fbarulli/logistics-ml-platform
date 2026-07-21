import mlflow
import pandas as pd

from logistics_ml.config import mlflow as mlflow_config


mlflow.set_tracking_uri(mlflow_config.tracking_uri)


def load_model():
    return mlflow.pyfunc.load_model(
        f"models:/{mlflow_config.registered_model_name}@{mlflow_config.champion_alias}"
    )


model = load_model()


def predict(payload: dict):
    df = pd.DataFrame([payload])

    prediction = model.predict(df)

    return {
        "trip_duration_minutes": float(prediction[0])
    }
