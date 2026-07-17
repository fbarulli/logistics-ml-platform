# src/logistics_ml/training.py
import argparse
import time

from logistics_ml.data import load_training_data
from logistics_ml.evaluation import evaluate
from logistics_ml.features import prepare_data
from logistics_ml.mlflow_utils import log_metrics, log_model, setup_mlflow
from logistics_ml.models import get_pipeline


EXPERIMENT_NAME = "taxi-duration-prediction"
REGISTERED_MODEL_NAME = "taxi-duration-model"
MODEL_ALIAS = "champion"


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
    pipeline = get_pipeline(model_name)
    start = time.time()
    pipeline.fit(X_train, y_train)
    training_time = time.time() - start
    print(f"Training completed in {training_time:.2f}s")
    return pipeline, training_time


def evaluate_model(model, X_test, y_test):
    metrics = evaluate(model, X_test, y_test)
    print("\nResults")
    print(f"MAE : {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"R²  : {metrics['r2']:.4f}")
    return metrics


def register_model(model, model_name, rows, training_time, metrics):
    log_metrics(
        model_name=model_name,
        rows=rows,
        training_time=training_time,
        metrics=metrics,
    )
    return log_model(
        model,
        REGISTERED_MODEL_NAME,
    )


def main():
    args = parse_args()
    print(f"Training model: {args.model}")
    setup_mlflow(EXPERIMENT_NAME)

    df = load_training_data()
    print(f"Loaded {len(df):,} rows")

    X_train, X_test, y_train, y_test = prepare_data(df)

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

    model_uri = register_model(
        model,
        args.model,
        len(df),
        training_time,
        metrics,
    )

    import mlflow

    client = mlflow.MlflowClient()

    versions = client.search_model_versions(
        f"name='{REGISTERED_MODEL_NAME}'"
    )

    version = int(
        max(
            versions,
            key=lambda x: int(x.version),
        ).version
    )

    client.set_registered_model_alias(
        name=REGISTERED_MODEL_NAME,
        alias=MODEL_ALIAS,
        version=version,
    )

    print("\n=== TRAINING COMPLETE ===")
    print(f"Model URI: {model_uri}")
    print(f"Champion version: {version}")


if __name__ == "__main__":
    main()
