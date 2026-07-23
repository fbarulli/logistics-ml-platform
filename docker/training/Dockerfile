FROM logistics-python-base:latest

WORKDIR /workspace

COPY . .

RUN uv pip install --no-deps -e .

COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py \
    /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

CMD ["python", "-m", "logistics_ml.training"]
