import mlflow
from mlflow import MlflowClient

client = MlflowClient()
print("=== MLflow Config ===")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Registry URI:", mlflow.get_registry_uri())

print("\n=== Registered Models ===")
models = client.search_registered_models()
for m in models:
    print(m.name)

print("\n=== Model Versions for taxi-duration-model ===")
try:
    versions = client.search_model_versions("name='taxi-duration-model'")
    for v in versions:
        print(f"Version {v.version} - {v.aliases}")
except Exception as e:
    print("Error:", e)
