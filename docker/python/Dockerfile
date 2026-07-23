FROM python:3.12-slim

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Dependency cache layer
COPY pyproject.toml .

RUN pip install --no-cache-dir -e .

# Application source
COPY src ./src

# Update editable install to point at current source
RUN pip install --no-deps -e .
