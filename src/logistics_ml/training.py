# src/logistics_ml/training.py

import argparse
import time

import mlflow

from logistics_ml.config.mlflow import mlflow as mlflow_config
from logistics_ml.data import load_training_data
from logistics_ml.evaluation import evaluate
from logistics_ml.features import prepare_dataset
from logistics_ml.mlflow_utils import (
    log_metrics,
    log_model,
    setup_mlflow,
)
from logistics_ml.models import get_model
from logistics_ml.models.pyfunc_wrapper import TaxiDurationPyfuncModel


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


def register_model(model, model_name, rows, training_time, metrics, input_example=None):

    log_metrics(
        model_name=model_name,
        rows=rows,
        training_time=training_time,
        metrics=metrics,
    )

    return log_model(
        model,
        mlflow_config.registered_model_name,
        input_example=input_example,
    )


def main():

    args = parse_args()

    print(f"Training model: {args.model}")

    setup_mlflow(
        mlflow_config.experiment_name,
    )

    df = load_training_data()

    print(f"Loaded {len(df):,} rows")

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

    wrapped_model = TaxiDurationPyfuncModel(pipeline, model)

    from logistics_ml.features import RAW_FEATURES

    input_example = df[RAW_FEATURES].head(5)

    model_uri = register_model(
        wrapped_model,
        args.model,
        len(df),
        training_time,
        metrics,
        input_example=input_example,
    )

    client = mlflow.MlflowClient()

    versions = client.search_model_versions(
        f"name='{mlflow_config.registered_model_name}'"
    )

    version = int(
        max(
            versions,
            key=lambda x: int(x.version),
        ).version
    )

    client.set_registered_model_alias(
        name=mlflow_config.registered_model_name,
        alias=mlflow_config.champion_alias,
        version=version,
    )

    print("=== TRAINING COMPLETE ===")
    print(f"Model URI: {model_uri}")
    print(f"Champion version: {version}")


if __name__ == "__main__":
    main()
