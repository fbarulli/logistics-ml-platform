# src/logistics_ml/training.py

import argparse
import time
from types import SimpleNamespace

from logistics_ml.config.mlflow import mlflow as mlflow_config
from logistics_ml.data import load_training_data
from logistics_ml.evaluation import evaluate
from logistics_ml.features import RAW_FEATURES, prepare_dataset
from logistics_ml.mlflow_utils import (
    promote_candidate,
    register_candidate,
    setup_mlflow,
)
from logistics_ml.models import get_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        choices=["linear", "rf", "xgb", "lgbm"],
        default="xgb",
    )
    return parser.parse_args()


def train_model(model_name, X_train, y_train):
    print("Starting training...")
    model = get_model(model_name)

    start = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start

    print(f"Training completed in {training_time:.2f}s")

    return model, training_time


def evaluate_model(model, X_test, y_test):
    metrics = evaluate(model, X_test, y_test)

    print("\nResults")
    print(f"MAE : {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"R²  : {metrics['r2']:.4f}")

    return metrics


def build_input_example(df):
    input_example = df[RAW_FEATURES].head(5).copy()

    input_example["pickup_location_id"] = (
        input_example["pickup_location_id"].astype("float64")
    )
    input_example["dropoff_location_id"] = (
        input_example["dropoff_location_id"].astype("float64")
    )

    return input_example


def main():
    args = parse_args()

    print(f"Training model: {args.model}")

    setup_mlflow(
        mlflow_config.experiment_name,
    )

    df = load_training_data()

    X_train, X_test, y_train, y_test, pipeline = prepare_dataset(df)

    model, training_time = train_model(
        args.model,
        X_train,
        y_train,
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test,
    )

    wrapped_model = SimpleNamespace(
        feature_pipeline=pipeline,
        model=model,
    )

    model_uri, version = register_candidate(
        model=wrapped_model,
        model_name=mlflow_config.registered_model_name,
        rows=len(df),
        training_time=training_time,
        metrics=metrics,
        input_example=build_input_example(df),
    )

    promote_candidate(
        model_name=mlflow_config.registered_model_name,
        alias=mlflow_config.champion_alias,
        version=version,
    )

    print("=== TRAINING COMPLETE ===")
    print(f"Model URI: {model_uri}")
    print(f"Champion version: {version}")


if __name__ == "__main__":
    main()
