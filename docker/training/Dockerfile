FROM python:3.12-slim

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY docker/training/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

RUN apt-get update && apt-get install -y git
ENV PYTHONPATH=/workspace/src

CMD ["python", "-m", "logistics_ml.training"]
