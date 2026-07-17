# ML Platform Handoff

## Current Status

### ✅ PostgreSQL

The MLflow database schema has been corrected and now matches MLflow 3.14.0.

```sql
SELECT version_num FROM alembic_version;
```

Returns:

```
b7e4c1a90f23
```

The relevant schema is now:

```sql
model_versions.version      -> character varying
model_version_tags.version  -> character varying
```

Both the MLflow server and training container are running:

```
mlflow==3.14.0
```

---

## MLflow

Training succeeds.

Example output:

```
Started run:
e8c184dbb671420e8e1fcad47b934889

Created version '2' of model 'taxi-duration-model'

Model URI:
models:/m-2e8f26e3f6b748dea49d713577aa1f5b
```

The registry contains:

```
taxi-duration-model
├── version 1
└── version 2
```

Verified using:

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

for mv in client.search_model_versions("name='taxi-duration-model'"):
    print(mv.name, mv.version, mv.status, mv.run_id)
```

This works inside the MLflow container.

---

## Registry Issue (Resolved)

Originally every registry lookup failed with:

```
operator does not exist:
integer = character varying
```

This was caused by an outdated database schema.

After fixing the schema, model registration and registry queries now work correctly.

Training successfully registers new model versions.

---

## Current Blocker

The API no longer fails because of the registry.

It now fails while loading artifacts.

Current error:

```
MlflowException:

Could not find an "MLmodel" configuration file at

/tmp/tmpxxxx/model/MLmodel
```

This occurs when attempting to load:

```python
runs:/e8c184dbb671420e8e1fcad47b934889/model
```

The same issue ultimately prevents:

```python
models:/taxi-duration-model/2
```

from working.

---

## Current Serving Code

Temporary debugging version:

```python
mlflow.set_tracking_uri("http://mlflow:5000")

model_uri = "runs:/e8c184dbb671420e8e1fcad47b934889/model"

model = mlflow.pyfunc.load_model(model_uri)
```

Eventually this should become:

```python
model_uri = "models:/taxi-duration-model/2"
```

---

## Important Discovery

Inside the API container:

```bash
find /mlflow/artifacts/1/e8c184dbb671420e8e1fcad47b934889
```

returns:

```
No such file or directory
```

This strongly suggests one of the following:

- the artifacts were never written
- the API is mounting a different Docker volume
- MLflow is serving artifacts from another backend
- the model artifact path differs from what the API expects

---

## Docker Compose

MLflow server starts with:

```
--backend-store-uri
postgresql+psycopg://logistics:logistics@postgres:5432/mlflow

--default-artifact-root
/mlflow/artifacts
```

API currently mounts:

```yaml
volumes:
  - .:/workspace
  - mlflow_artifacts:/mlflow/artifacts
```

Need to verify that this is the exact same Docker volume mounted by the MLflow server.

---

## Things Already Verified

✅ PostgreSQL is healthy

✅ MLflow server is healthy

✅ Training logs metrics

✅ Training logs models

✅ Model registry creates new versions

✅ Registry queries succeed inside the MLflow container

✅ API reaches the MLflow server

✅ API reaches the registry

❌ API cannot load model artifacts

---

## Next Debugging Steps

### 1. Verify artifacts actually exist

Inside the MLflow container:

```bash
find /mlflow/artifacts -name MLmodel
```

If no MLmodel files exist anywhere, then training never persisted artifacts.

---

### 2. Compare Docker mounts

Inspect both containers:

```bash
docker inspect mlflow-server
docker inspect taxi-api
```

Compare:

```
Mounts
```

for:

```
/mlflow/artifacts
```

They must point to the exact same Docker volume.

---

### 3. If MLflow also lacks artifacts

Investigate where `log_model()` actually writes the model.

Print:

```python
mlflow.get_artifact_uri()
```

after logging.

---

### 4. If MLflow has artifacts but API does not

Fix the shared Docker volume configuration.

---

### 5. Restore normal serving

Once

```python
runs:/...
```

loads successfully, switch back to:

```python
models:/taxi-duration-model/2
```

and remove all temporary debugging code.

---

## Overall Assessment

The original MLflow registry/database issue appears to be resolved.

The remaining blocker is now entirely related to artifact storage.

Model registration succeeds.

The registry contains the correct model versions.

The API reaches the registry successfully.

However, the API cannot locate the underlying MLmodel artifact required to load the model.

The investigation should now focus exclusively on artifact storage, Docker volumes, and MLflow artifact paths rather than PostgreSQL or the model registry.
