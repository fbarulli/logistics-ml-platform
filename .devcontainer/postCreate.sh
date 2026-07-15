#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo "🚀 Setting up Logistics ML Platform"
echo "========================================"

echo ""
echo "📦 Tool versions"
echo "----------------------------------------"

python --version
uv --version
git --version
docker --version
kubectl version --client
helm version --short
kind version
java -version

echo ""
echo "----------------------------------------"

# Initialize a uv project if one doesn't already exist
if [ ! -f "pyproject.toml" ]; then
    echo "No pyproject.toml found."
    echo "Initializing a new uv project..."

    uv init --name logistics-ml-platform

    echo "Project initialized."
else
    echo "Existing pyproject.toml found."
fi

echo ""

# Install dependencies if they exist
if [ -f "pyproject.toml" ]; then
    echo "Syncing Python environment..."
    uv sync
fi

echo ""

mkdir -p \
    data \
    notebooks \
    src \
    tests \
    producer \
    consumer \
    api \
    model \
    flink \
    airflow \
    k8s

echo "Project folders ready."

echo ""
echo "========================================"
echo "✅ Dev Container Ready!"
echo "========================================"

echo ""
echo "Useful commands:"
echo ""
echo "  uv add <package>"
echo "  uv sync"
echo "  docker compose up -d"
echo "  kind create cluster"
echo ""