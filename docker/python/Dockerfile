FROM logistics-python-base:latest

WORKDIR /workspace

COPY pyproject.toml .
COPY src ./src

RUN pip install --no-cache-dir --no-deps -e .
