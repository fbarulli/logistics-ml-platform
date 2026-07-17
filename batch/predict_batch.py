import sys
import pandas as pd
import mlflow
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_NAME = "taxi-duration-model"

def load_champion_model():
    model_uri = f"models:/{MODEL_NAME}@champion"
    logger.info(f"Loading model from {model_uri}")
    model = mlflow.pyfunc.load_model(model_uri)
    logger.info("Champion model loaded successfully")
    return model

def predict_batch(input_path: str, output_path: str):
    model = load_champion_model()
    
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} records from {input_path}")
    
    # Feature order must match training pipeline (from features.py)
    feature_order = [
        "passenger_count",
        "pickup_location_id",
        "dropoff_location_id",
        "pickup_hour",
        "pickup_day_of_week",
        "pickup_month",
        "trip_distance"
    ]
    
    # Ensure all required columns exist
    missing = [f for f in feature_order if f not in df.columns]
    if missing:
        raise ValueError(f"Missing features: {missing}")
    
    X = df[feature_order]
    
    predictions = model.predict(X)
    df['predicted_duration'] = predictions
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"✅ Predictions saved to {output_path} ({len(df)} records)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python predict_batch.py <input.csv> <output.csv>")
        sys.exit(1)
    predict_batch(sys.argv[1], sys.argv[2])
