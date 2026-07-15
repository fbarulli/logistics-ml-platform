import argparse
import time
import mlflow

import pandas as pd

from sqlalchemy import create_engine

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from lightgbm import LGBMRegressor
from xgboost import XGBRegressor


DATABASE_URL = (
    "postgresql+psycopg://logistics:logistics@postgres:5432/logistics"
)

mlflow.set_tracking_uri(
    "http://mlflow:5000"
)

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
        help="Model to train",
    )

    return parser.parse_args()


def load_data():

    print("Loading training data...")

    engine = create_engine(DATABASE_URL)

    df = pd.read_sql(
        """
        SELECT *
        FROM training_data
        """,
        engine,
    )

    print(f"Loaded {len(df):,} rows")

    return df


def get_pipeline(model_name: str):

    if model_name == "linear":

        model = LinearRegression()

    elif model_name == "rf":

        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            max_samples=0.3,
            n_jobs=-1,
            random_state=42,
        )

    elif model_name == "xgb":

        model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            tree_method="hist",
            random_state=42,
            n_jobs=-1,
        )

    elif model_name == "lgbm":

        model = LGBMRegressor(
            n_estimators=300,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
        )

    else:
        raise ValueError(
            f"Unknown model: {model_name}"
        )

    pipeline = Pipeline(
        [
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "model",
                model,
            ),
        ]
    )

    return pipeline


def prepare_data(df):

    features = [
        "passenger_count",
        "pickup_location_id",
        "dropoff_location_id",
        "pickup_hour",
        "pickup_day_of_week",
        "pickup_month",
        "trip_distance",
    ]

    target = "trip_duration_minutes"

    X = df[features]

    y = df[target]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )


def evaluate(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
        squared=False,
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def main():

    args = parse_args()

    model_name = args.model

    print(
        f"Training model: {model_name}"
    )

    # MLflow setup

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    df = load_data()

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = prepare_data(df)

    pipeline = get_pipeline(
        model_name
    )

    with mlflow.start_run(
        run_name=model_name
    ):

        start = time.time()

        pipeline.fit(
            X_train,
            y_train,
        )

        training_time = (
            time.time() - start
        )

        metrics = evaluate(
            pipeline,
            X_test,
            y_test,
        )

        print("\nResults")

        print(
            f"MAE : {metrics['mae']:.2f}"
        )

        print(
            f"RMSE: {metrics['rmse']:.2f}"
        )

        print(
            f"R²  : {metrics['r2']:.4f}"
        )

        mlflow.log_param(
            "model",
            model_name,
        )

        mlflow.log_param(
            "rows",
            len(df),
        )

        mlflow.log_metric(
            "mae",
            metrics["mae"],
        )

        mlflow.log_metric(
            "rmse",
            metrics["rmse"],
        )

        mlflow.log_metric(
            "r2",
            metrics["r2"],
        )

        mlflow.log_metric(
            "training_seconds",
            training_time,
        )

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name=REGISTERED_MODEL_NAME,
        )

        print(
            "Model logged to MLflow"
        )


if __name__ == "__main__":
    main()
