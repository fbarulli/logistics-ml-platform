ARG BASE_IMAGE=logistics-python-base:latest
FROM ${BASE_IMAGE}

WORKDIR /workspace

COPY pyproject.toml .
COPY src ./src

RUN pip install --no-cache-dir --no-deps -e .
