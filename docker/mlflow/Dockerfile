#docker/mlflow/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY docker/mlflow/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /mlflow/artifacts

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "postgresql+psycopg://logistics:logistics@postgres:5432/mlflow", "--default-artifact-root", "/mlflow/artifacts", "--allowed-hosts", "*"]
