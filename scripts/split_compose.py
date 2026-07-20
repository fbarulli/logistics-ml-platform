from pathlib import Path
import shutil

root = Path("/workspace")

compose = root / "docker-compose.yml"
backup = root / "docker-compose.yml.bak"

if compose.exists():
    shutil.copy2(compose, backup)
    print(f"✓ Backed up docker-compose.yml -> {backup.name}")

root_compose = """\
include:
  - docker-compose.apps.yml
  - docker-compose.streaming.yml
"""

apps = """\
services:

  postgres:
    build:
      context: .
      dockerfile: docker/postgres/Dockerfile
    container_name: logistics-postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mlflow:
    build:
      context: .
      dockerfile: docker/mlflow/Dockerfile
    container_name: mlflow-server
    ports:
      - "5000:5000"
    volumes:
      - mlflow_artifacts:/mlruns

  api:
    build:
      context: .
      dockerfile: service/Dockerfile
    container_name: taxi-api

    depends_on:
      - postgres
      - mlflow

    ports:
      - "8000:8000"

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 10

  producer:
    build:
      context: .
      dockerfile: producer/Dockerfile

    container_name: taxi-producer

    depends_on:
      - kafka

    volumes:
      - .:/workspace

  consumer:
    build:
      context: .
      dockerfile: consumer/Dockerfile

    container_name: taxi-consumer

    depends_on:
      kafka:
        condition: service_started
      api:
        condition: service_healthy

    volumes:
      - .:/workspace

volumes:

  postgres_data:

  mlflow_artifacts:
    external: true
    name: logistics-ml-platform_mlflow_artifacts
"""

streaming = """\
services:

  kafka:
    image: apache/kafka:3.8.0

    container_name: taxi-kafka

    ports:
      - "9092:9092"

    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1

  jobmanager:
    build:
      context: .
      dockerfile: docker/flink/Dockerfile

    container_name: taxi-jobmanager

    command: jobmanager

    ports:
      - "8081:8081"

    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: jobmanager

    volumes:
      - ./flink/sql:/opt/flink/sql

  taskmanager:
    build:
      context: .
      dockerfile: docker/flink/Dockerfile

    container_name: taxi-taskmanager

    command: taskmanager

    depends_on:
      - jobmanager

    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: jobmanager
        taskmanager.numberOfTaskSlots: 2

    volumes:
      - ./flink/sql:/opt/flink/sql

  sql-gateway:
    image: flink:1.20-java17

    container_name: taxi-sql-gateway

    depends_on:
      - jobmanager

    entrypoint:
      - /opt/flink/bin/sql-gateway.sh

    command:
      - start-foreground
      - -Dsql-gateway.endpoint.rest.address=0.0.0.0

    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        sql-gateway.endpoint.rest.address: 0.0.0.0
        sql-gateway.endpoint.rest.port: 8083

    ports:
      - "8083:8083"

    volumes:
      - ./flink/sql:/opt/flink/sql
"""

(root / "docker-compose.yml").write_text(root_compose)
(root / "docker-compose.apps.yml").write_text(apps)
(root / "docker-compose.streaming.yml").write_text(streaming)

print()
print("✓ Created docker-compose.yml")
print("✓ Created docker-compose.apps.yml")
print("✓ Created docker-compose.streaming.yml")

print()
print("Next commands:")
print("--------------")
print("docker compose config")
print("docker compose up --build")
