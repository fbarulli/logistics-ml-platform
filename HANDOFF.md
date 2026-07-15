# Logistics ML Platform - Handoff

## Goal

Build a production-style logistics ML platform inspired by a Just Eat Takeaway ML Engineer stack.

Target technologies:

- Python
- uv
- PostgreSQL
- SQLAlchemy
- Alembic
- LightGBM
- XGBoost
- MLflow
- Kafka
- Flink
- FastAPI
- Kubernetes


# Current Status

## Development Environment

Running inside:

VS Code Dev Container

Project:

/workspaces/logistics-ml-platform

Python:

3.12.13

Package manager:

uv


# Project Structure

Current:

logistics-ml-platform/

├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── postCreate.sh
│
├── data/
│   └── raw/
│
├── k8s/
│
├── scripts/
│
├── src/
│
├── tests/
│
├── pyproject.toml
└── uv.lock


# Kubernetes Setup

## Kind Cluster

Created:

logistics-ml

Verify:

kubectl get nodes

Result:

NAME                         STATUS
logistics-ml-control-plane   Ready


# Kubernetes Networking Fix

Problem:

kubeconfig pointed to:

https://host.docker.internal:37709

Inside Linux dev container:

host.docker.internal was unavailable.

Fixed:

Replace:

host.docker.internal

with:

172.18.0.1


Verify:

kubectl get nodes


# PostgreSQL Deployment

## Namespace

Created:

kubectl create namespace database


Verify:

kubectl get ns


---

## PostgreSQL Secret

File:

k8s/postgres-secret.yaml


Contains:

DATABASE=logistics
USER=logistics
PASSWORD=logistics


Applied:

kubectl apply -f k8s/postgres-secret.yaml


---

## Persistent Storage

File:

k8s/postgres-pvc.yaml


Storage:

10Gi


Storage class:

standard

rancher.io/local-path


Initial state:

Pending

Reason:

WaitForFirstConsumer


Expected behavior.

PVC binds after pod creation.


---

## PostgreSQL Deployment

File:

k8s/postgres-deployment.yaml


Image:

postgres:17


Configuration:

- 1 replica
- Persistent volume
- Readiness probe
- Liveness probe
- Resource requests
- Resource limits


Resources:

requests:
  cpu: 250m
  memory: 512Mi

limits:
  cpu: 1000m
  memory: 1Gi


Applied:

kubectl apply -f k8s/postgres-deployment.yaml


Status:

deployment "postgres" successfully rolled out


---

## PostgreSQL Service

File:

k8s/postgres-service.yaml


Service:

postgres


Namespace:

database


Type:

ClusterIP


Port:

5432


Verify:

kubectl get svc -n database


Current:

postgres   ClusterIP   10.96.216.47   5432/TCP


---

# PostgreSQL Verification

Connected:

kubectl exec -it -n database deployment/postgres -- psql -U logistics -d logistics


Verified:

SELECT version();


Result:

PostgreSQL 17.10
aarch64


Database currently empty:

\dt


Result:

Did not find any relations.


# Next Task

## SQLAlchemy + Alembic Setup


Install:

uv add sqlalchemy alembic psycopg[binary]


Initialize:

uv run alembic init alembic


Next steps:

1. Create SQLAlchemy models.
2. Configure Alembic connection.
3. Create first migration.
4. Apply schema to PostgreSQL.
5. Load taxi dataset.
6. Build SQL feature engineering pipeline.
7. Train LightGBM/XGBoost.
8. Add MLflow.
9. Add Kafka.
10. Add Flink.
11. Deploy services to Kubernetes.


# Final Architecture

Taxi Dataset

        |
        v

PostgreSQL

        |
        v

SQL Feature Engineering

        |
        v

LightGBM / XGBoost

        |
        v

MLflow

        |
        v

FastAPI

        |
        v

Kafka

        |
        v

Flink

        |
        v

Kubernetes


# Resume Point

Start next session with:

uv add sqlalchemy alembic psycopg[binary]

Then:

uv run alembic init alembic
