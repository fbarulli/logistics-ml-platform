FROM python:3.12-slim

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py \
    /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

CMD ["python", "-m", "logistics_ml.training"]
