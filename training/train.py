import argparse
import time
import mlflow
import mlflow.sklearn
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

DATABASE_URL = "postgresql+psycopg://logistics:logistics@localhost:5432/logistics"

parser = argparse.ArgumentParser()

parser.add_argument(
    "--model",
    choices=["linear", "rf", "xgb", "lgbm"],
    default="xgb",
    help="Model to train",
)

args = parser.parse_args()

MODEL_NAME = args.model


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
        )

    elif model_name == "lgbm":
        model = LGBMRegressor(
            n_estimators=300,
            learning_rate=0.1,
            random_state=42,
        )

    else:
        raise ValueError(f"Unknown model: {model_name}")

    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("model", model),
        ]
    )


def main():
    mlflow.set_experiment("taxi-fare-prediction")

    engine = create_engine(DATABASE_URL)

    print("Loading training data...")

    # Sample for classical models
    if MODEL_NAME in ("linear", "rf"):
        query = """
        SELECT *
        FROM training_data
        TABLESAMPLE SYSTEM (10)
        """
    else:
        query = "SELECT * FROM training_data"

    df = pd.read_sql(query, engine)

    X = df[
        [
            "passenger_count",
            "pickup_location_id",
            "dropoff_location_id",
            "pickup_hour",
            "pickup_day_of_week",
            "pickup_month",
            "trip_distance",
        ]
    ]

    y = df["fare_amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline = get_pipeline(MODEL_NAME)

    with mlflow.start_run(run_name=MODEL_NAME) as run:

        start = time.time()

        pipeline.fit(X_train, y_train)

        train_time = time.time() - start

        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5
        r2 = r2_score(y_test, predictions)

        print(f"MAE : {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R²  : {r2:.4f}")

        # Parameters
        mlflow.log_param("model", MODEL_NAME)
        mlflow.log_param("rows", len(df))

        if hasattr(pipeline.named_steps["model"], "get_params"):
            mlflow.log_params(pipeline.named_steps["model"].get_params())

        # Metrics
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("training_time_seconds", train_time)

        # Save model artifact
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
        )

        # Register model in MLflow Model Registry
        model_uri = f"runs:/{run.info.run_id}/model"

        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name="taxi-fare-predictor",
        )

        print(f"\nRegistered model: {registered_model.name}")
        print(f"Version: {registered_model.version}")


if __name__ == "__main__":
    main()
