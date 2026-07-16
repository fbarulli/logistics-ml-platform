# Logistics ML Platform – Handoff

## Current Goal

Build a production-style ML platform similar to what companies like JET Germany would operate.

The focus is **not** just training a model, but building the surrounding platform:

* ETL
* PostgreSQL
* Feature Engineering
* Model Training
* MLflow
* FastAPI Serving
* Airflow
* Streaming
* Kubernetes

---

# Current Architecture

```
Developer
    │
    ▼
VS Code Dev Container
    │
    ▼
Docker Engine
    │
    ├── postgres
    ├── mlflow
    ├── etl
    └── training
```

Current repository:

```
docker/
    postgres/
    mlflow/
    etl/
    training/

src/
    logistics_ml/

data/
notebooks/
tests/
scripts/

docker-compose.yml
Makefile
```

---

# Dataset

NYC Taxi January 2024

Target:

```
trip_duration_minutes
```

Features:

* passenger_count
* pickup_location_id
* dropoff_location_id
* pickup_hour
* pickup_day_of_week
* pickup_month
* trip_distance

Rows:

```
8,938,099
```

Average duration

```
14.95 minutes
```

---

# Models Tested

## Linear Regression

MAE

```
2.56
```

RMSE

```
5.25
```

R²

```
0.9069
```

---

## Random Forest

MAE

```
1.97
```

RMSE

```
4.35
```

R²

```
0.9363
```

Too memory intensive.

Crashes the training instance.

Not chosen.

---

## XGBoost

MAE

```
1.99
```

RMSE

```
4.92
```

R²

```
0.9184
```

Chosen.

Reason:

* much faster
* scalable
* production friendly

---

## LightGBM

MAE

```
1.97
```

RMSE

```
4.79
```

R²

```
0.9226
```

Very close to XGBoost.

Will revisit later if needed.

---

# Why XGBoost

Although RF scored slightly higher,

XGBoost trains significantly faster and is much more realistic for production.

Current platform uses

```
XGBRegressor
```

---

# MLflow

MLflow is no longer running inside the development environment.

It has its own container.

Current architecture:

```
postgres
↓

mlflow server

↓

training container
```

Training logs:

* parameters
* metrics
* artifacts

to the MLflow server.

---

# PostgreSQL

Current databases

```
logistics
mlflow
```

Both created successfully.

---

# Docker Containers

## postgres

Owns

* logistics database
* mlflow database

---

## mlflow

Owns

* experiment tracking
* model registry
* artifacts

Runs on

```
5000
```

Backend

```
postgresql+psycopg://logistics:logistics@postgres:5432/mlflow
```

Artifact root

```
/mlflow/artifacts
```

---

## etl

Responsible for

* loading parquet
* preprocessing
* loading PostgreSQL

---

## training

Responsible for

* reading training_data
* training model
* logging MLflow

---

# Current Compose

Services

```
postgres
mlflow
etl
training
```

Persistent volumes

```
postgres_data
mlflow_artifacts
```

---

# Makefile

Target direction

```
make build

make up

make load

make train

make down
```

Goal

```
git clone

make up

make load

make train
```

Nothing else.

---

# Important Docker Decision

During development

DO NOT copy Python files into the image every edit.

Instead

mount the repository.

Reason

Image

contains

* Python
* libraries
* dependencies

Repository mount

contains

live source code.

Editing

```
train.py
```

should never require rebuilding the image.

Only changes to

* Dockerfile
* requirements.txt
* system libraries

should require

```
docker compose build
```

---

# Repository Refactor Started

Created

```
src/logistics_ml/
```

Current plan

```
config.py

db.py

models.py

features.py

utils.py
```

---

## config.py

Single source of truth

Contains

```
DATABASE_URL

MLFLOW_TRACKING_URI

RANDOM_STATE
```

---

## db.py

Contains

```
engine = create_engine(...)
```

Every module imports

```
from logistics_ml.db import engine
```

No duplicated database code.

---

# Training Refactor

Goal

train.py should only orchestrate

1. parse args

2. load data

3. get pipeline

4. fit

5. evaluate

6. log MLflow

Business logic moves into

```
src/logistics_ml
```

---

# Dev Container

Uses Docker Outside Docker.

Current issue

MLflow is healthy.

Verified:

* container running
* database connected
* Docker network reachable
* HTTP returns 200 inside container network

Remaining issue

VS Code Dev Container port forwarding.

Need to add

```
forwardPorts

5000

5432
```

to

```
.devcontainer/devcontainer.json
```

then rebuild the Dev Container.

Infrastructure itself is healthy.

---

# Important Decision

Do NOT install MLflow inside the development environment.

Training should always execute inside

```
training container
```

Reason

Avoid dependency conflicts involving

* pandas
* pyarrow
* MLflow
* uv

Each container owns its dependencies.

---

# Desired Future Layout

```
docker/

    postgres/

    mlflow/

    etl/

    training/


src/

    logistics_ml/

        config.py

        db.py

        models.py

        features.py

        training.py

        serving.py

        utils.py


tests/

data/

notebooks/

docker-compose.yml

Makefile
```

Eventually

```
docker/training/train.py
```

should become

```
python -m logistics_ml.training
```

leaving Dockerfiles responsible only for infrastructure.

---

# Remaining Work

## Infrastructure

* Finish repository cleanup
* Move reusable code into src/logistics_ml
* Fix Dev Container port forwarding
* Remove duplicate training scripts

---

## Data

* Automate schema creation
* Make ETL completely reproducible

---

## ML

* Feature engineering
* Hyperparameter tuning
* Feature importance
* SHAP analysis

---

## Platform

Implement

FastAPI

↓

Batch inference

↓

MLflow Model Registry

↓

Airflow

↓

Streaming (Kafka/Flink)

↓

Monitoring

↓

Kubernetes deployment

---

# Long-Term Vision

The objective is to finish with a platform that resembles a production ML system:

```
ETL
    ↓
PostgreSQL
    ↓
Feature Engineering
    ↓
Training
    ↓
MLflow
    ↓
Model Registry
    ↓
FastAPI
    ↓
Batch Predictions
    ↓
Streaming Predictions
    ↓
Monitoring
    ↓
Kubernetes
```

The emphasis is on demonstrating production ML engineering practices rather than only achieving the highest predictive accuracy.
