import argparse
import time

from logistics_ml.data import load_training_data
from logistics_ml.evaluation import evaluate
from logistics_ml.features import prepare_data
from logistics_ml.mlflow_utils import (
    log_metrics,
    log_model,
    setup_mlflow,
)
from logistics_ml.models import get_pipeline


EXPERIMENT_NAME = "taxi-duration-prediction"
REGISTERED_MODEL_NAME = "taxi-duration-model"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        choices=[
            "linear",
            "rf",
            "xgb",
            "lgbm",
        ],
        default="xgb",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Training model: {args.model}")

    setup_mlflow(EXPERIMENT_NAME)

    df = load_training_data()

    print(f"Loaded {len(df):,} rows")

    X_train, X_test, y_train, y_test = prepare_data(df)

    pipeline = get_pipeline(args.model)

    print("Starting training...")

    start = time.time()

    pipeline.fit(
        X_train,
        y_train,
    )

    training_time = time.time() - start

    print(
        f"Training completed in {training_time:.2f}s"
    )

    metrics = evaluate(
        pipeline,
        X_test,
        y_test,
    )

    print("\nResults")
    print(f"MAE : {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"R²  : {metrics['r2']:.4f}")

    log_metrics(
        model_name=args.model,
        rows=len(df),
        training_time=training_time,
        metrics=metrics,
    )

    model_uri = log_model(
        pipeline,
        REGISTERED_MODEL_NAME,
    )

    print("\n=== TRAINING COMPLETE ===")
    print("Model URI:")
    print(model_uri)


if __name__ == "__main__":
    main()
