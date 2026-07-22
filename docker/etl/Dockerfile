#docker/etl/Dockerfile
FROM python:3.12-slim
WORKDIR /workspace
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*
COPY docker/etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data/raw/taxi_zone_lookup.csv data/raw/taxi_zone_lookup.csv
ENV PYTHONPATH=/workspace/src
CMD ["python", "-m", "logistics_ml.etl.run"]
