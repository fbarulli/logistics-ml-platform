#service/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY docker/patches/sqlalchemy_store.py /tmp/

RUN cp /tmp/sqlalchemy_store.py \
    /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

ENV PYTHONPATH=/workspace/src

COPY service/app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
