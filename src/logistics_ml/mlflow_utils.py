import traceback

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


def setup_mlflow(experiment_name):
    print("=== MLFLOW SETUP ===")
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_registry_uri("http://mlflow:5000")
    print("Tracking URI:", mlflow.get_tracking_uri())
    print("Registry URI:", mlflow.get_registry_uri())

    experiment = mlflow.set_experiment(experiment_name)
    print("Experiment ID:", experiment.experiment_id)

    run = mlflow.start_run()
    print("Run ID:", run.info.run_id)
    return run.info.run_id


def log_metrics(model_name, rows, training_time, metrics):
    print("=== LOG METRICS ===")

    run = mlflow.active_run()

    print("Active run:")
    print(run)

    if run:
        print("Run ID:")
        print(run.info.run_id)

    mlflow.log_param("model", model_name)
    mlflow.log_param("rows", rows)
    mlflow.log_metric("training_time", training_time)

    for key, value in metrics.items():
        mlflow.log_metric(key, float(value))

    print("Metrics logged")


def log_model(model, model_name):
    print("=== LOG MODEL ===")

    run = mlflow.active_run()

    print("Active run:")
    print(run)

    if run:
        print("Run ID:")
        print(run.info.run_id)

        print("Artifact URI (active run):")
        print(run.info.artifact_uri)

        print("mlflow.get_artifact_uri():")
        print(mlflow.get_artifact_uri())

    print("Logging model...")

    try:
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name=model_name,
            skops_trusted_types=[
                "numpy.dtype",
                "xgboost.core.Booster",
                "xgboost.sklearn.XGBRegressor",
                "logistics_ml.models.xgboost.XGBoostModel",
            ],
        )
    except Exception:
        print("\n=== log_model() EXCEPTION ===")
        traceback.print_exc()
        raise

    print("Model logged")

    print("Model URI:")
    print(model_info.model_uri)

    print("=== VERIFY ARTIFACTS ===")

    if run:
        client = MlflowClient()

        refreshed_run = client.get_run(run.info.run_id)

        print("Stored artifact URI:")
        print(refreshed_run.info.artifact_uri)

        try:
            artifacts = client.list_artifacts(run.info.run_id)

            if artifacts:
                for artifact in artifacts:
                    print(
                        "Artifact:",
                        artifact.path,
                        "Directory:",
                        artifact.is_dir,
                    )
            else:
                print("No artifacts returned by list_artifacts().")
        except Exception:
            print("\n=== list_artifacts() EXCEPTION ===")
            traceback.print_exc()

    print("=== VERIFY REGISTERED MODEL ===")

    versions = client.search_model_versions(
        f"name='{model_name}'"
    )

    for version in versions:
        print(
            "Model:",
            version.name,
            "Version:",
            version.version,
            "Status:",
            version.status,
            "Run ID:",
            version.run_id,
            "Source:",
            version.source,
        )

    return model_info.model_uri
