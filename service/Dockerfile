FROM python:3.12-slim

WORKDIR /app

COPY service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .
COPY src ./src
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install .

COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py \
    /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py



COPY service/app.py .
COPY src ./src

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
