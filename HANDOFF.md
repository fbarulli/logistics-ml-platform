# Logistics ML Platform — Project Handoff

## Current Status

The core end-to-end ML inference platform is operational.

Architecture:

```
Producer
    │
    ▼
Kafka (taxi-trips)
    │
    ▼
Consumer
    │
    ▼
FastAPI (/predict)
    │
    ▼
MLflow Model Registry (Champion alias)
    │
    ▼
Prediction
    │
    ▼
PostgreSQL (taxi_predictions)
```

---

# Stack

- Python 3.12
- FastAPI
- PostgreSQL
- Kafka
- MLflow
- Docker Compose
- scikit-learn
- XGBoost
- SQLAlchemy
- psycopg3

Upcoming:

- Flink SQL
- Feast

---

# Current Project Structure

```
.
├── consumer/
├── producer/
├── service/
├── src/logistics_ml/
├── docker/
├── flink/
│   └── sql/
└── docker-compose.yml
```

---

# Infrastructure

Running services:

- postgres
- kafka
- mlflow
- api
- producer
- consumer

Training and ETL are run on demand.

---

# Databases

## logistics

Contains

```
locations
taxi_trips
taxi_predictions
```

## mlflow

Contains

- experiments
- runs
- registered models
- model versions

---

# MLflow

Tracking URI

```
http://mlflow:5000
```

Registered model

```
taxi-duration-model
```

Alias

```
champion
```

Current version

```
2
```

API loads

```
models:/taxi-duration-model@champion
```

(or resolves champion to Version 2)

---

# Current Pipeline

Producer generates events:

```
TaxiTripEvent
```

Schema

```
trip_id
pickup_zone
dropoff_zone
distance_km
passengers
timestamp
```

Consumer

- consumes Kafka
- validates with Pydantic
- derives model features
- calls FastAPI
- stores predictions

API

- loads champion model from MLflow
- predicts duration
- returns JSON

Predictions stored in

```
taxi_predictions
```

Example

```
trip_id
prediction
created_at
```

Current row count exceeded 800+ rows.

---

# Docker Notes

Consumer depends on

```
depends_on:
  kafka:
    condition: service_started
  api:
    condition: service_healthy
```

API has healthcheck enabled.

Producer and Consumer use

```
context: .
dockerfile: producer/Dockerfile

context: .
dockerfile: consumer/Dockerfile
```

Both mount

```
.:/workspace
```

and use

```
PYTHONPATH=/workspace/src
```

---

# Important Fixes Already Made

✔ PostgreSQL initialization

✔ MLflow registry

✔ Champion alias

✔ API model loading

✔ Producer imports

✔ Consumer imports

✔ psycopg installation

✔ API health dependency

✔ Prediction persistence

✔ Docker build contexts

✔ Kafka connectivity

---

# Verified End-to-End

Verified working chain:

```
Producer

↓

Kafka

↓

Consumer

↓

API

↓

MLflow

↓

Prediction

↓

Postgres
```

Verified via

```
SELECT COUNT(*) FROM taxi_predictions;
```

and

```
SELECT *
FROM taxi_predictions
ORDER BY id DESC
LIMIT 10;
```

API logs show repeated

```
POST /predict
200 OK
```

---

# Next Phase

## Phase 1

Flink SQL

Goal:

Move feature engineering out of Python and into Flink.

New architecture

```
Producer

↓

Kafka
(taxi-trips)

↓

Flink SQL

↓

Kafka
(taxi-features)

↓

Consumer

↓

API

↓

Postgres
```

Producer remains unchanged.

Consumer becomes thinner.

---

## Planned Flink SQL Directory

```
flink/sql/

01-source.sql

02-features.sql

03-sink.sql

run.sql
```

Two Kafka topics

```
taxi-trips

taxi-features
```

Flink computes

```
pickup_hour

pickup_day_of_week

pickup_month

trip_distance

passenger_count

pickup_location_id

dropoff_location_id
```

Consumer will read

```
taxi-features
```

instead of

```
taxi-trips
```

---

# Phase 2

Feast

Goal

Online Feature Store.

Architecture

```
Producer

↓

Kafka

↓

Flink SQL

↓

Feast Online Store

↓

API

↓

Prediction
```

API will no longer derive features.

Instead

```
feast.get_online_features(...)
```

feeds the model.

---

# Later Roadmap

- Drift monitoring
- Prometheus
- Grafana
- Retraining pipeline
- CI/CD
- Kubernetes
- Helm
- GitHub Actions
- Feature monitoring
- Model monitoring

---

# Overall Goal

Build a production-quality Real-Time ML Inference Platform demonstrating:

- Data Engineering
- Streaming
- Feature Engineering
- MLOps
- Model Serving
- Online Inference
- MLflow Registry
- Kafka
- Flink SQL
- Feast
- Docker
- PostgreSQL

Target profile:

Senior Machine Learning Engineer / MLOps Engineer.
