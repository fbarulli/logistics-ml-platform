FROM logistics-python-base:latest

WORKDIR /workspace

COPY docker/patches/sqlalchemy_store.py /tmp/sqlalchemy_store.py

RUN cp /tmp/sqlalchemy_store.py \
    /usr/local/lib/python3.12/site-packages/mlflow/store/model_registry/sqlalchemy_store.py

RUN mkdir -p /mlflow/artifacts

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "postgresql+psycopg://logistics:logistics@postgres:5432/mlflow", "--default-artifact-root", "/mlflow/artifacts", "--allowed-hosts", "*"]
